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
        self.round_number = 0
        self.test_player_id = None

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

    def add_test_player(self):
        if len(self.players) >= self.max_players:
            return False
        test_id = 999999999
        self.test_player_id = test_id
        self.players[test_id] = {
            "name": "🤖 Test Player",
            "cards": [get_random_card() for _ in range(6)],
            "lives": True
        }
        return True

    def start_game(self):
        if len(self.players) < 2:
            return False
        self.current_leader = random.choice(list(self.players.keys()))  # Random first leader
        self.round_number = 1
        return True

    async def show_hand(self, interaction: discord.Interaction, player_id: int):
        """Show hand privately to a player"""
        if player_id not in self.players:
            return
        player = self.players[player_id]
        embed = discord.Embed(title=f"Your Hand ({len(player['cards'])} cards) - Round {self.round_number}", color=0x00FF00)
        for i, (name, stats) in enumerate(player["cards"]):
            embed.add_field(
                name=f"{i}. {name}",
                value=f"**STR** {stats['Strength']} | **AGI** {stats['Agility']}\n"
                      f"**INT** {stats['Intelligence']} | **CUT** {stats['Cuteness']}\n"
                      f"**VOL** {stats['Volume']} | **BAN** {stats['Banana Affinity']}",
                inline=False
            )
        user = await interaction.client.fetch_user(player_id)
        try:
            await user.send(embed=embed)
        except:
            pass  # Can't DM user

    async def play_card(self, interaction: discord.Interaction, stat: str):
        await interaction.response.defer()

        # Auto-play for all players
        for player_id in list(self.players.keys()):
            player = self.players[player_id]
            if not player["cards"]:
                continue
            if player_id in self.played_cards:
                continue

            card_index = random.randint(0, len(player["cards"]) - 1)
            card = player["cards"].pop(card_index)
            self.played_cards[player_id] = card

            embed = discord.Embed(title=f"💪 {player['name']} played **{card[0]}**", color=0xFFD700)
            embed.set_image(url=card[1]["image"])
            embed.add_field(name="Stats", value=f"**STR** {card[1]['Strength']} | **AGI** {card[1]['Agility']}\n"
                                                f"**INT** {card[1]['Intelligence']} | **CUT** {card[1]['Cuteness']}\n"
                                                f"**VOL** {card[1]['Volume']} | **BAN** {card[1]['Banana Affinity']}", inline=False)
            await interaction.followup.send(embed=embed)

        # Resolve round
        if len(self.played_cards) > 0:
            await self.resolve_round(interaction, stat)

    async def resolve_round(self, interaction: discord.Interaction, stat: str):
        if not self.played_cards:
            return

        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        won_cards = list(self.played_cards.values())

        self.players[winner_id]["cards"].extend(won_cards)

        winner_name = self.players[winner_id]["name"]
        await interaction.followup.send(f"🏆 **{winner_name}** wins the round with **{stat}**!")

        self.current_leader = winner_id
        self.played_cards.clear()
        self.round_number += 1

        await self.show_remaining_cards(interaction)

        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            await interaction.followup.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪")

    async def show_remaining_cards(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"📊 Round {self.round_number} — Remaining Cards", color=0x00FF88)
        embed.description = f"**Next Leader:** {self.players[self.current_leader]['name']}\n\n"

        for player in self.players.values():
            names = ", ".join([c[0] for c in player["cards"]]) if player["cards"] else "No cards left"
            embed.add_field(
                name=f"{player['name']} — {len(player['cards'])} cards",
                value=names[:400] + ("..." if len(names) > 400 else ""),
                inline=False
            )
        await interaction.followup.send(embed=embed)
