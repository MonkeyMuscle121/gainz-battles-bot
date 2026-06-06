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
        self.game_over = False

    def add_player(self, player_id, name):
        if self.game_over:
            self.reset_game()  # Auto reset if previous game ended
        if len(self.players) >= self.max_players:
            return False
        if player_id in self.players:
            return False
        self.players[player_id] = {
            "name": name,
            "cards": [get_random_card() for _ in range(4)],
            "lives": True
        }
        return True

    def reset_game(self):
        """Reset for new game"""
        self.players = {}
        self.current_leader = None
        self.played_cards = {}
        self.round_number = 0
        self.game_over = False

    def start_game(self):
        if len(self.players) < 2:
            return False
        self.current_leader = random.choice(list(self.players.keys()))
        self.round_number = 1
        self.game_over = False
        return True

    async def deal_round_cards(self, interaction: discord.Interaction):
        self.played_cards = {}

        for pid, player in self.players.items():
            if not player["cards"]:
                continue

            card_index = random.randint(0, len(player["cards"]) - 1)
            card = player["cards"].pop(card_index)
            self.played_cards[pid] = card

            # Auto show only to leader
            if pid == self.current_leader:
                embed = discord.Embed(title=f"Round {self.round_number} • Your Card", color=0x00FF00)
                embed.set_image(url=card[1]["image"])
                embed.add_field(name=card[0], value="This is your card for this round", inline=False)
                try:
                    await interaction.followup.send(embed=embed, ephemeral=True)
                except:
                    pass

    async def show_card(self, interaction: discord.Interaction):
        if interaction.user.id not in self.played_cards:
            await interaction.response.send_message("No card dealt yet. Use `/start` first.", ephemeral=True)
            return

        card = self.played_cards[interaction.user.id]
        embed = discord.Embed(title=f"Round {self.round_number} • Your Card", color=0x00FF00)
        embed.set_image(url=card[1]["image"])
        embed.add_field(name=card[0], value="This is your card for this round", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def play_card(self, interaction: discord.Interaction, stat: str):
        await interaction.response.defer()

        if interaction.user.id != self.current_leader:
            await interaction.followup.send("❌ Only the current leader can choose the stat!", ephemeral=True)
            return

        await interaction.followup.send(f"**Round {self.round_number}** — Stat Chosen: **{stat}**")

        for pid, card in self.played_cards.items():
            player_name = self.players[pid]["name"]
            embed = discord.Embed(title=f"💪 {player_name} played **{card[0]}**", color=0xFFD700)
            embed.set_image(url=card[1]["image"])
            await interaction.followup.send(embed=embed)

        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        winner_name = self.players[winner_id]["name"]

        won_cards = list(self.played_cards.values())
        self.players[winner_id]["cards"].extend(won_cards)

        await interaction.followup.send(f"🏆 **{winner_name}** wins the round with **{stat}**!")

        self.current_leader = winner_id
        self.played_cards.clear()
        self.round_number += 1

        await self.deal_round_cards(interaction)

        # Game over check + auto reset
        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            await interaction.followup.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪")
            self.game_over = True
            # Auto reset for new game
            await interaction.followup.send("🔄 Game has been reset. Use `/join` to start a new game!")

    # Keep your existing show_card and other methods
