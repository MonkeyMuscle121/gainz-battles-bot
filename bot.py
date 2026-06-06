# game.py
import random
import discord
import asyncio
from cards import get_random_card, MONKEY_CARDS

class GainzBattlesGame:
    def __init__(self):
        self.players = {}
        self.current_leader = None
        self.played_cards = {}
        self.max_players = 4
        self.round_number = 0
        self.timer_task = None

    def add_player(self, player_id, name):
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

    def add_test_player(self):
        if len(self.players) >= self.max_players:
            return False
        test_id = 999999999
        self.players[test_id] = {
            "name": "🤖 Test Player",
            "cards": [get_random_card() for _ in range(4)],
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
        self.played_cards = {}
        available = list(MONKEY_CARDS.items())
        random.shuffle(available)

        for i, pid in enumerate(self.players.keys()):
            player = self.players[pid]
            if not player["cards"]:
                continue
            card_name, card_data = available[i % len(available)]
            self.played_cards[pid] = (card_name, card_data.copy())

            embed = discord.Embed(title=f"Round {self.round_number} • Your Card", color=0x00FF00)
            embed.set_image(url=card_data["image"])
            embed.add_field(name=card_name, value="This is your card for this round", inline=False)

            try:
                await interaction.followup.send(embed=embed, ephemeral=True)
            except:
                pass

        # Start 2-minute timer for leader
        if self.timer_task:
            self.timer_task.cancel()
        self.timer_task = asyncio.create_task(self.auto_play_timer(interaction))

    async def auto_play_timer(self, interaction: discord.Interaction):
        try:
            await asyncio.sleep(120)  # 2 minutes
            if self.played_cards and self.current_leader not in [list(self.played_cards.keys())[0] if self.played_cards else None]:
                # Auto choose random stat
                stats = ["Strength", "Agility", "Intelligence", "Cuteness", "Volume", "Banana Affinity"]
                auto_stat = random.choice(stats)
                await interaction.channel.send(f"⏰ Time's up! Auto-playing with **{auto_stat}**")
                # Trigger play with auto stat
                await self.play_card_auto(auto_stat)
        except asyncio.CancelledError:
            pass

    async def play_card_auto(self, stat: str):
        # This would need interaction, simplified version
        pass  # We'll handle in main play_card for now

    async def play_card(self, interaction: discord.Interaction, stat: str):
        await interaction.response.defer()

        if interaction.user.id != self.current_leader:
            await interaction.followup.send("❌ Only the current leader can choose the stat!", ephemeral=True)
            return

        if self.timer_task:
            self.timer_task.cancel()

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

        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            await interaction.followup.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪")
