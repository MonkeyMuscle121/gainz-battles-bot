# game.py
import random
import discord
import asyncio
from cards import MONKEY_CARDS

class GainzBattlesGame:
    def __init__(self):
        self.players = {}
        self.current_leader = None
        self.played_cards = {}
        self.max_players = 4
        self.round_number = 0
        self.viewed_cards = set()
        self.game_active = True

    def add_player(self, player_id, name):
        if not self.game_active or len(self.players) >= self.max_players:
            return False
        if player_id in self.players:
            return False
        self.players[player_id] = {
            "name": name,
            "cards": [],
            "lives": True
        }
        return True

    def add_test_player(self):
        if len(self.players) >= self.max_players:
            return False
        test_id = 999999999
        self.players[test_id] = {
            "name": "THE BOT",
            "cards": [],
            "lives": True
        }
        return True

    def reset_game(self):
        self.players = {}
        self.current_leader = None
        self.played_cards = {}
        self.round_number = 0
        self.viewed_cards = set()
        self.game_active = True

    def start_game(self):
        if len(self.players) < 2:
            return False

        all_cards = list(MONKEY_CARDS.items())
        random.shuffle(all_cards)

        card_index = 0
        for pid, player in self.players.items():
            player["cards"] = []
            for _ in range(5):
                if card_index < len(all_cards):
                    card_name, card_data = all_cards[card_index]
                    player["cards"].append((card_name, card_data.copy()))
                    card_index += 1

        self.current_leader = random.choice(list(self.players.keys()))
        self.round_number = 1
        self.viewed_cards = set()
        self.game_active = True
        return True

    async def deal_round_cards(self, interaction: discord.Interaction):
        self.played_cards = {}
        self.viewed_cards = set()

        for pid, player in self.players.items():
            if not player["cards"]:
                continue
            card = player["cards"].pop(0)
            self.played_cards[pid] = card

            # Auto-view for THE BOT
            if pid == 999999999:
                self.viewed_cards.add(pid)

        # If THE BOT is the leader, auto-play after short delay
        if self.current_leader == 999999999:
            asyncio.create_task(self._bot_auto_play(interaction))

    async def _bot_auto_play(self, interaction: discord.Interaction):
        await asyncio.sleep(4)  # Give time for message to show

        stats = ["Strength", "Agility", "Intelligence", "Cuteness", "Volume", "Banana Affinity"]
        stat = random.choice(stats)

        await interaction.channel.send(f"🤖 **THE BOT** chose **{stat}**")

        # Run the full round logic
        await self._execute_play(stat, interaction)

    async def show_card(self, interaction: discord.Interaction):
        if interaction.user.id not in self.played_cards:
            await interaction.response.send_message("No card dealt yet. Use `/start` first.", ephemeral=True)
            return

        card = self.played_cards[interaction.user.id]
        embed = discord.Embed(title=f"Round {self.round_number} • Your Card", color=0x00FF00)
        embed.set_image(url=card[1]["image"])
        embed.add_field(name=card[0], value="This is your card for this round", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        self.viewed_cards.add(interaction.user.id)

        if len(self.viewed_cards) == len([p for p in self.players.values() if len(p["cards"]) > 0]):
            leader_name = self.players[self.current_leader]['name']
            await interaction.followup.send(
                f"✅ **All active users have now seen their cards.**\n"
                f"The lead player **{leader_name}** choose your stat with `/play`"
            )

    async def _execute_play(self, stat: str, interaction: discord.Interaction):
        await interaction.channel.send(f"**Round {self.round_number}** — **THE BOT** chose **{stat}**\n\nAll users cards now shown below...")

        await asyncio.sleep(5)

        for pid, card in self.played_cards.items():
            player_name = self.players[pid]["name"]
            embed = discord.Embed(title=f"💪 {player_name} played **{card[0]}**", color=0xFFD700)
            embed.set_image(url=card[1]["image"])
            await interaction.channel.send(embed=embed)

        await asyncio.sleep(5)

        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        winner_name = self.players[winner_id]["name"]

        roast_lines = [
            "got absolutely BODIED 💀",
            "is built like a wet noodle",
            "should stick to peeling bananas",
            "just got sent to the zoo",
            "is crying in the corner eating reject bananas",
            "needs to hit the gym",
            "is the definition of 'all talk, no gains'"
        ]
        roast = random.choice(roast_lines)

        won_cards = list(self.played_cards.values())
        self.players[winner_id]["cards"].extend(won_cards)

        await interaction.channel.send(f"🏆 **{winner_name}** wins the round with **{stat}**!\n"
                                        f"The rest of you {roast}")

        self.current_leader = winner_id
        self.played_cards.clear()
        self.round_number += 1
        self.viewed_cards = set()

        await asyncio.sleep(5)

        await interaction.channel.send("**All active players:** Type `/card` to see your next round card!")

        await self.deal_round_cards(interaction)

        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            await interaction.channel.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪\n"
                                            f"The rest of you are officially banished to the weak monkey enclosure 🐒💀")
            self.reset_game()

    async def play_card(self, interaction: discord.Interaction, stat: str):
        await interaction.response.defer()

        if interaction.user.id != self.current_leader:
            await interaction.followup.send("❌ Only the current leader can choose the stat!", ephemeral=True)
            return

        if len(self.viewed_cards) < len([p for p in self.players.values() if len(p["cards"]) > 0]):
            await interaction.followup.send("❌ All active players must use `/card` first!", ephemeral=True)
            return

        await self._execute_play(stat, interaction)
