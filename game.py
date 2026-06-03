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
        self.current_leader = list(self.players.keys())[0]
        self.round_number = 1
        return True

    async def play_card(self, interaction: discord.Interaction, card_index: int, stat: str):
        await interaction.response.defer()

        player_id = interaction.user.id
        if player_id not in self.players:
            await interaction.followup.send("❌ You are not in the game!", ephemeral=True)
            return

        player = self.players[player_id]

        if player_id in self.played_cards:
            await interaction.followup.send("❌ You already played this round!", ephemeral=True)
            return

        if card_index < 0 or card_index >= len(player["cards"]):
            await interaction.followup.send("❌ Invalid card index!", ephemeral=True)
            return

        card = player["cards"].pop(card_index)
        self.played_cards[player_id] = card

        embed = discord.Embed(title=f"💪 {player['name']} played **{card[0]}**", color=0xFFD700)
        embed.set_image(url=card[1]["image"])
        embed.add_field(name="Stats", value=f"**STR** {card[1]['Strength']} | **AGI** {card[1]['Agility']}\n"
                                            f"**INT** {card[1]['Intelligence']} | **CUT** {card[1]['Cuteness']}\n"
                                            f"**VOL** {card[1]['Volume']} | **BAN** {card[1]['Banana Affinity']}", inline=False)
        await interaction.followup.send(embed=embed)

        # Auto play for test player
        if self.test_player_id and self.test_player_id not in self.played_cards:
            await self.auto_play_test_player(interaction, stat)

        active = len([p for p in self.players.values() if len(p["cards"]) > 0])
        if len(self.played_cards) == active:
            await self.resolve_round(interaction, stat.capitalize())

    async def auto_play_test_player(self, interaction: discord.Interaction, stat: str):
        if not self.test_player_id or self.test_player_id not in self.players:
            return
        test_player = self.players[self.test_player_id]
        if not test_player["cards"]:
            return
        card_index = random.randint(0, len(test_player["cards"]) - 1)
        card = test_player["cards"].pop(card_index)
        self.played_cards[self.test_player_id] = card

        embed = discord.Embed(title=f"🤖 Test Player played **{card[0]}**", color=0xAAAAAA)
        embed.set_image(url=card[1]["image"])
        embed.add_field(name="Stats", value=f"**STR** {card[1]['Strength']} | **AGI** {card[1]['Agility']}\n"
                                            f"**INT** {card[1]['Intelligence']} | **CUT** {card[1]['Cuteness']}\n"
                                            f"**VOL** {card[1]['Volume']} | **BAN** {card[1]['Banana Affinity']}", inline=False)
        await interaction.followup.send(embed=embed)

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
