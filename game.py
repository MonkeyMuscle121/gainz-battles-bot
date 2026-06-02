# game.py
import random
import discord
from cards import get_random_card

class GainzBattlesGame:
    def __init__(self):
        self.players = {}
        self.current_leader = None
        self.played_cards = {}
        self.max_players = 4

    def add_player(self, player_id, name):
        if len(self.players) >= self.max_players:
            return False
        if player_id in self.players:
            return False
        self.players[player_id] = {
            "name": name,
            "cards": [get_random_card() for _ in range(6)],
            "lives": True
        }
        return True

    def start_game(self):
        if len(self.players) < 2:
            return False
        self.current_leader = list(self.players.keys())[0]
        return True

    async def play_card(self, ctx, card_index: int, stat: str):
        player_id = ctx.author.id
        if player_id not in self.players:
            await ctx.send("❌ You are not in the game!")
            return

        player = self.players[player_id]
        if card_index < 0 or card_index >= len(player["cards"]):
            await ctx.send("❌ Invalid card number!")
            return

        card = player["cards"].pop(card_index)
        self.played_cards[player_id] = card

        embed = discord.Embed(title=f"💪 {player['name']} played **{card[0]}**", color=0xFFD700)
        embed.set_image(url=card[1]["image"])
        embed.add_field(name="Stats", value=f"**STR** {card[1]['Strength']} | **AGI** {card[1]['Agility']}\n"
                                            f"**INT** {card[1]['Intelligence']} | **CUT** {card[1]['Cuteness']}\n"
                                            f"**VOL** {card[1]['Volume']} | **BAN** {card[1]['Banana Affinity']}", inline=False)
        await ctx.send(embed=embed)

        active = len([p for p in self.players.values() if len(p["cards"]) > 0])
        if len(self.played_cards) == active:
            await self.resolve_round(ctx, stat.capitalize())

    async def resolve_round(self, ctx, stat):
        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        won_cards = list(self.played_cards.values())
        self.players[winner_id]["cards"].extend(won_cards)

        await ctx.send(f"🏆 **{self.players[winner_id]['name']}** wins the round with **{stat}**!")

        self.played_cards.clear()
        self.current_leader = winner_id

        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            winner_name = self.players[winner_id]["name"]
            await ctx.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪")
