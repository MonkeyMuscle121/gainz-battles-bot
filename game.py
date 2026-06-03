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

    async def play_card(self, interaction: discord.Interaction, card_index: int, stat: str):
        """Handles playing a card when using slash command"""
        player_id = interaction.user.id
        if player_id not in self.players:
            await interaction.followup.send("❌ You are not in the game!", ephemeral=True)
            return

        player = self.players[player_id]
        if card_index < 0 or card_index >= len(player["cards"]):
            await interaction.followup.send("❌ Invalid card number! Use `/hand` to check your cards.", ephemeral=True)
            return

        # Play the card
        card = player["cards"].pop(card_index)
        self.played_cards[player_id] = card

        # Show the played card publicly
        embed = discord.Embed(
            title=f"💪 {player['name']} played **{card[0]}**",
            color=0xFFD700
        )
        embed.set_image(url=card[1]["image"])
        embed.add_field(
            name="Stats",
            value=f"**STR** {card[1]['Strength']} | **AGI** {card[1]['Agility']}\n"
                  f"**INT** {card[1]['Intelligence']} | **CUT** {card[1]['Cuteness']}\n"
                  f"**VOL** {card[1]['Volume']} | **BAN** {card[1]['Banana Affinity']}",
            inline=False
        )
        await interaction.followup.send(embed=embed)

        # Check if all active players have played
        active_players = len([p for p in self.players.values() if len(p["cards"]) > 0])
        if len(self.played_cards) == active_players:
            await self.resolve_round(interaction, stat.capitalize())

    async def resolve_round(self, interaction: discord.Interaction, stat: str):
        if not self.played_cards:
            return

        # Find winner
        winner_id = max(self.played_cards.keys(), key=lambda pid: self.played_cards[pid][1].get(stat, 0))
        won_cards = list(self.played_cards.values())

        self.players[winner_id]["cards"].extend(won_cards)

        await interaction.followup.send(f"🏆 **{self.players[winner_id]['name']}** wins the round with **{stat}**!")

        self.played_cards.clear()
        self.current_leader = winner_id

        # Check if game is over
        remaining = [p for p in self.players.values() if len(p["cards"]) > 0]
        if len(remaining) <= 1:
            winner_name = self.players[winner_id]["name"]
            await interaction.followup.send(f"🎉 **GAME OVER! {winner_name} is the $GAINZ CHAMPION!** 💪")
