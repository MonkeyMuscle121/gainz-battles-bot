# bot.py
import discord
from discord import app_commands
from discord.ext import commands
import os
from game import GainzBattlesGame

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f"💪 $GAINZ BATTLES Bot is online as {bot.user}")

@bot.tree.command(name="sync", description="Sync slash commands")
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        await bot.tree.sync(guild=interaction.guild)
        await bot.tree.sync()
        await interaction.followup.send("✅ Commands synced!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)

@bot.tree.command(name="addtest", description="Add test player")
async def addtest(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        await interaction.response.send_message("Use `/join` first!", ephemeral=True)
        return
    game = games[channel_id]
    if game.add_test_player():
        await interaction.response.send_message("🤖 Test Player added!")
    else:
        await interaction.response.send_message("Game full!", ephemeral=True)

@bot.tree.command(name="join", description="Join the game")
async def join(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        games[channel_id] = GainzBattlesGame()
    game = games[channel_id]
    if game.add_player(interaction.user.id, interaction.user.display_name):
        await interaction.response.send_message(f"💪 {interaction.user.mention} joined! ({len(game.players)}/4)")
    else:
        await interaction.response.send_message("Game full or already joined!", ephemeral=True)

@bot.tree.command(name="start", description="Start the game")
async def start(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        await interaction.response.send_message("Use `/join` first!", ephemeral=True)
        return
    game = games[channel_id]
    if game.start_game():
        await interaction.response.send_message(f"🎮 Game Started! Leader: **{game.players[game.current_leader]['name']}**")
    else:
        await interaction.response.send_message("Need 2+ players!", ephemeral=True)

@bot.tree.command(name="hand", description="View your hand")
async def hand(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game or interaction.user.id not in game.players:
        await interaction.response.send_message("Not in game!", ephemeral=True)
        return
    player = game.players[interaction.user.id]
    embed = discord.Embed(title=f"Your Hand ({len(player['cards'])} cards)", color=0x00FF00)
    for i, (name, stats) in enumerate(player["cards"]):
        embed.add_field(name=f"{i}. {name}", value=f"STR:{stats['Strength']} AGI:{stats['Agility']}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# SIMPLIFIED PLAY - Only choose stat, bot picks random card
@bot.tree.command(name="play", description="Choose stat - bot picks random card")
@app_commands.describe(stat="Stat to battle with")
@app_commands.choices(stat=[
    app_commands.Choice(name="Strength", value="Strength"),
    app_commands.Choice(name="Agility", value="Agility"),
    app_commands.Choice(name="Intelligence", value="Intelligence"),
    app_commands.Choice(name="Cuteness", value="Cuteness"),
    app_commands.Choice(name="Volume", value="Volume"),
    app_commands.Choice(name="Banana Affinity", value="Banana Affinity")
])
async def play(interaction: discord.Interaction, stat: str):
    game = games.get(interaction.channel.id)
    if not game:
        await interaction.response.send_message("No game running!", ephemeral=True)
        return
    await game.play_card(interaction, stat)

@bot.tree.command(name="leaderboard", description="Show leaderboard")
async def leaderboard(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game:
        await interaction.response.send_message("No game running!", ephemeral=True)
        return
    embed = discord.Embed(title="💪 Leaderboard", color=0xFFD700)
    for p in game.players.values():
        embed.add_field(name=p["name"], value=f"Cards: {len(p['cards'])}", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
