# bot.py
import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from game import GainzBattlesGame

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f"💪 $GAINZ BATTLES Bot is online as {bot.user}")

@bot.command(name="resetcommands")
async def resetcommands(ctx):
    await ctx.send("🔄 Resetting commands...")
    try:
        bot.tree.clear_commands(guild=ctx.guild)
        await bot.tree.sync(guild=ctx.guild)
        await bot.tree.sync()
        await ctx.send("✅ Commands reset!")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.tree.command(name="join", description="Join the game")
async def join(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        games[channel_id] = GainzBattlesGame()
    game = games[channel_id]

    was_empty = len(game.players) == 0

    if game.add_player(interaction.user.id, interaction.user.display_name):
        await interaction.response.send_message(f"💪 {interaction.user.mention} joined! ({len(game.players)}/4)")

        if was_empty:
            await interaction.followup.send("⏰ **Game will auto start in 1 minute...**")
            asyncio.create_task(auto_start_game(channel_id, interaction))
    else:
        await interaction.response.send_message("Game full or already joined!", ephemeral=True)

async def auto_start_game(channel_id, original_interaction):
    await asyncio.sleep(60)  # 1 minute

    if channel_id not in games:
        return
    game = games[channel_id]

    if game.current_leader is not None:
        return

    if len(game.players) == 1:
        game.add_test_player()
        await original_interaction.channel.send("🤖 **Test Player** added automatically!")

    if game.start_game():
        leader_name = game.players[game.current_leader]['name']
        await original_interaction.channel.send(
            f"🎮 **$GAINZ BATTLES AUTO STARTED!**\n"
            f"First leader: **{leader_name}**\n\n"
            f"**All players:** Type `/card` to see your round card! dont fck about (you have 15 seconds) before autoplay, At Any time use command /leaderboard for scores"
        )
        await game.deal_round_cards(original_interaction)

@bot.tree.command(name="start", description="Manually start the game")
async def start(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    if channel_id not in games:
        games[channel_id] = GainzBattlesGame()
    game = games[channel_id]

    if game.players and game.current_leader is not None:
        await interaction.response.send_message("❌ A game is already running! you melt", ephemeral=True)
        return

    if len(game.players) == 1:
        game.add_test_player()
        await interaction.channel.send("🤖 **Test Player** added automatically!")

    if game.start_game():
        leader_name = game.players[game.current_leader]['name']
        await interaction.response.send_message(
            f"🎮 **$GAINZ BATTLES STARTED!**\n"
            f"First leader: **{leader_name}**\n\n"
            f"**All players:** Type `/card` to see your round card! (you have 15 seconds)"
        )
        await game.deal_round_cards(interaction)
    else:
        await interaction.response.send_message("Need at least 1 player!", ephemeral=True)

@bot.tree.command(name="card", description="View your current round card")
async def card(interaction: discord.Interaction):
    game = games.get(interaction.channel.id)
    if not game:
        await interaction.response.send_message("No game running!", ephemeral=True)
        return
    await game.show_card(interaction)

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
        status = " ❌" if len(p["cards"]) == 0 else ""
        embed.add_field(name=f"{p['name']}{status}", value=f"Cards: {len(p['cards'])}", inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
