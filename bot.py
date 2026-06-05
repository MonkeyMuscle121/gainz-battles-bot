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

# ====================== RESET ======================
@bot.command(name="resetcommands")
async def resetcommands(ctx):
    await ctx.send("🔄 **Full command reset in progress...**")
    try:
        bot.tree.clear_commands(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)
        await bot.tree.sync()
        await ctx.send("✅ **Commands fully reset!**\n\n**Please:**\n1. Completely close Discord (task manager)\n2. Reopen Discord\n3. Wait 30 seconds")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# ====================== GAME COMMANDS ======================

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
        await interaction.response.send_message(f"🎮 **$GAINZ BATTLES STARTED!**\nFirst leader: **{game.players[game.current_leader]['name']}**\n\n**All players:** Type `/card` to see your round card!")
        await game.deal_round_cards(interaction)
    else:
        await interaction.response.send_message("Need at least 2 players!", ephemeral=True)

@bot.tree.command(name="card", description="View your current round card")
async def card(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game or interaction.user.id not in game.played_cards:
        await interaction.response.send_message("No card dealt yet. Use `/start` first.", ephemeral=True)
        return
    
    card = game.played_cards[interaction.user.id]
    embed = discord.Embed(title=f"Round {game.round_number} • Your Card", color=0x00FF00)
    embed.set_image(url=card[1]["image"])
    embed.add_field(name=card[0], value="This is your card for this round", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="play", description="Choose stat (Leader only)")
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
    embed = discord.Embed(title="💪 $GAINZ BATTLES Leaderboard", color=0xFFD700)
    for p in game.players.values():
        embed.add_field(name=p["name"], value=f"Cards: {len(p['cards'])}", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
