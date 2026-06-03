# bot.py
import discord
from discord import app_commands
from discord.ext import commands
import os
from cards import get_all_cards
from game import GainzBattlesGame

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

games = {}  # channel_id : game instance

@bot.event
async def on_ready():
    print(f"💪 $GAINZ BATTLES Bot is online as {bot.user}")
    print("Attempting to sync commands...")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} global commands.")
    except Exception as e:
        print(f"Sync error: {e}")

# ====================== MANUAL SYNC COMMAND ======================
@bot.tree.command(name="sync", description="Force sync all slash commands")
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        # Guild sync (fast)
        guild_synced = await bot.tree.sync(guild=interaction.guild)
        # Global sync
        global_synced = await bot.tree.sync()
        
        await interaction.followup.send(
            f"✅ **Commands Synced!**\n\n"
            f"• Guild: {len(guild_synced)} commands\n"
            f"• Global: {len(global_synced)} commands\n\n"
            f"Please wait 1-2 minutes and restart Discord app if needed.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Sync failed: {e}", ephemeral=True)

# ====================== TEST PLAYER ======================
@bot.tree.command(name="addtest", description="Add a test player for solo testing")
async def addtest(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        await interaction.response.send_message("Please use `/join` first!", ephemeral=True)
        return

    game = games[channel_id]
    if game.add_test_player():
        await interaction.response.send_message("🤖 **Test Player** added! You can now `/start` the game.")
    else:
        await interaction.response.send_message("❌ Game is full (max 4).", ephemeral=True)

# ====================== MAIN GAME COMMANDS ======================

@bot.tree.command(name="join", description="Join the $GAINZ BATTLES game")
async def join(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        games[channel_id] = GainzBattlesGame()
    
    game = games[channel_id]
    if game.add_player(interaction.user.id, interaction.user.display_name):
        await interaction.response.send_message(f"💪 {interaction.user.mention} joined the battle! ({len(game.players)}/4)")
    else:
        await interaction.response.send_message("❌ Game is full or you're already in!", ephemeral=True)

@bot.tree.command(name="start", description="Start the $GAINZ BATTLES game")
async def start(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        await interaction.response.send_message("Use `/join` first!", ephemeral=True)
        return
    game = games[channel_id]
    if game.start_game():
        await interaction.response.send_message(f"🎮 **$GAINZ BATTLES STARTED!**\nFirst leader: **{game.players[game.current_leader]['name']}**")
    else:
        await interaction.response.send_message("Need at least 2 players!", ephemeral=True)

@bot.tree.command(name="hand", description="View your cards (private)")
async def hand(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game or interaction.user.id not in game.players:
        await interaction.response.send_message("You're not in a game!", ephemeral=True)
        return
    player = game.players[interaction.user.id]
    embed = discord.Embed(title=f"Your Hand ({len(player['cards'])} cards)", color=0x00FF00)
    for i, (name, stats) in enumerate(player["cards"]):
        embed.add_field(name=f"{i}. {name}", value=f"STR:{stats['Strength']} AGI:{stats['Agility']}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="play", description="Play a card")
@app_commands.describe(card_index="Card number (0-5)", stat="Stat to use")
@app_commands.choices(stat=[
    app_commands.Choice(name="Strength", value="Strength"),
    app_commands.Choice(name="Agility", value="Agility"),
    app_commands.Choice(name="Intelligence", value="Intelligence"),
    app_commands.Choice(name="Cuteness", value="Cuteness"),
    app_commands.Choice(name="Volume", value="Volume"),
    app_commands.Choice(name="Banana Affinity", value="Banana Affinity")
])
async def play(interaction: discord.Interaction, card_index: int, stat: str):
    game = games.get(interaction.channel.id)
    if not game:
        await interaction.response.send_message("No game running!", ephemeral=True)
        return
    await game.play_card(interaction, card_index, stat)

@bot.tree.command(name="leaderboard", description="Show leaderboard")
async def leaderboard(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game:
        await interaction.response.send_message("No game running!", ephemeral=True)
        return
    embed = discord.Embed(title="💪 $GAINZ Leaderboard", color=0xFFD700)
    for p in game.players.values():
        embed.add_field(name=p["name"], value=f"Cards: {len(p['cards'])}", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
