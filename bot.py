# bot.py
import discord
from discord.ext import commands
import os
from cards import get_all_cards
from game import GainzBattlesGame

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

games = {}

@bot.event
async def on_ready():
    print(f"💪 $GAINZ BATTLES Bot is online as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.channel.id not in games:
        games[ctx.channel.id] = GainzBattlesGame()
    game = games[ctx.channel.id]
    if game.add_player(ctx.author.id, ctx.author.display_name):
        await ctx.send(f"💪 {ctx.author.mention} joined! ({len(game.players)}/4)")
    else:
        await ctx.send("❌ Game full or already joined!")

@bot.command()
async def start(ctx):
    if ctx.channel.id not in games:
        await ctx.send("Do `!join` first!")
        return
    game = games[ctx.channel.id]
    if game.start_game():
        await ctx.send(f"🎮 **$GAINZ BATTLES STARTED!** First leader: **{game.players[game.current_leader]['name']}**")
    else:
        await ctx.send("Need at least 2 players!")

@bot.command()
async def hand(ctx):
    game = games.get(ctx.channel.id)
    if not game or ctx.author.id not in game.players:
        await ctx.send("You're not in a game!")
        return
    player = game.players[ctx.author.id]
    embed = discord.Embed(title=f"Your Hand ({len(player['cards'])} cards)", color=0x00FF00)
    for i, (name, stats) in enumerate(player["cards"]):
        embed.add_field(name=f"{i}. {name}", value=f"STR:{stats['Strength']} AGI:{stats['Agility']}", inline=False)
    await ctx.author.send(embed=embed)

@bot.command()
async def play(ctx, card_index: int, stat: str):
    game = games.get(ctx.channel.id)
    if not game:
        await ctx.send("No game running!")
        return
    await game.play_card(ctx, card_index, stat)

@bot.command()
async def leaderboard(ctx):
    game = games.get(ctx.channel.id)
    if not game:
        await ctx.send("No game running!")
        return
    embed = discord.Embed(title="💪 Leaderboard", color=0xFFD700)
    for p in game.players.values():
        embed.add_field(name=p["name"], value=f"Cards left: {len(p['cards'])}", inline=False)
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
