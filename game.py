# game.py
import random
import discord
from cards import get_random_card

class GainzBattlesGame:
    def __init__(self):
        self.players = {}
        self.current_leader = None
        self.played_cards = {}   # Secret until reveal
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
        self.current_leader = random.choice(list(self.players.keys()))
        self.round_number = 1
        return True

    async def deal_round_cards(self, interaction: discord.Interaction):
        """Secretly pick one card per player at start of round"""
        self.played_cards = {}
        for pid in self.players:
            player = self.players[pid]
            if not player["cards"]:
                continue
            card_index = random.randint(0, len(player["cards"]) - 1)
            card = player["cards"].pop(card_index)
            self.played_cards[pid] = card

            # Show privately to the player
            embed = discord.Embed(title="Your Card for this Round", color=0x00FF00)
            embed.set_image(url=card[1]["image"])
            embed.add_field(name=card[0], value=f"STR:{card[1]['Strength']} AGI:{card[1]['Agility']}\nINT:{card[1]['Intelligence']} CUT:{card[1]['Cuteness']}", inline=False)
            try:
                user = await interaction.client.fetch_user(pid)
                await user.send(embed=embed)
            except:
                pass

    async def play_card(self, interaction: discord.Interaction, stat: str):
        await interaction.response.defer()

        if interaction.user.id != self.current_leader:
            await interaction.followup.send("❌ Only the current leader can choose the stat!", ephemeral=True)
            return

        # Reveal all secretly chosen cards
        await interaction.followup.send(f"**Round {self.round_number}** — Stat: **{stat}**")

        for pid, card in self.played_cards.items():
            player_name = self.players[pid]["name"]
            embed = discord.Embed(title=f"💪 {player_name} played **{card[0]}**", color=0xFFD700)
            embed.set_image(url=card[1]["image"])
            await interaction.followup.send(embed=embed)

        # Determine winner
        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        winner_name = self.players[winner_id]["name"]

        # Winner takes cards
        won_cards = list(self.played_cards.values())
        self.players[winner_id]["cards"].extend(won_cards)

        await interaction.followup.send(f"🏆 **{winner_name}** wins the round with **{stat}**!")

        self.current_leader = winner_id
        self.played_cards.clear()
        self.round_number += 1

        await self.show_remaining_cards(interaction)

        # Check game over
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
