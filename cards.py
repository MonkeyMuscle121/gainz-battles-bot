# cards.py
import random

MONKEY_CARDS = {
    "MANDRILL MAULER": {
        "Strength": 88, "Agility": 70, "Intelligence": 92, "Volume": 62,
        "Cuteness": 40, "Banana Affinity": 78,
        "image": "https://raw.githubusercontent.com/YOUR_USERNAME/gainz-battles-bot/main/cards/mandrill-mauler.jpg"
    },
    "CHIMPANZEE CHAMPION": {
        "Strength": 85, "Agility": 88, "Intelligence": 82, "Volume": 80,
        "Cuteness": 35, "Banana Affinity": 70,
        "image": "https://raw.githubusercontent.com/YOUR_USERNAME/gainz-battles-bot/main/cards/chimpanzee-champion.jpg"
    },
    # ... (I will give you the FULL version with all 28 cards below)
}

def get_random_card():
    name = random.choice(list(MONKEY_CARDS.keys()))
    return name, MONKEY_CARDS[name].copy()

def get_all_cards():
    return MONKEY_CARDS
