# cards.py
import random

MONKEY_CARDS = {
    "MANDRILL MAULER": {
        "Strength": 88, "Agility": 70, "Intelligence": 92, "Volume": 62,
        "Cuteness": 40, "Banana Affinity": 78,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/mandrill-mauler.jpg"
    },
    "CHIMPANZEE CHAMPION": {
        "Strength": 85, "Agility": 88, "Intelligence": 82, "Volume": 80,
        "Cuteness": 35, "Banana Affinity": 70,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/chimpanzee-champion.jpg"
    },
    "SPIDERMONKEY SAVAGE": {
        "Strength": 72, "Agility": 95, "Intelligence": 88, "Volume": 65,
        "Cuteness": 50, "Banana Affinity": 75,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/spidermonkey-savage.jpg"
    },
    "GORILLA GOLIATH": {
        "Strength": 95, "Agility": 68, "Intelligence": 75, "Volume": 88,
        "Cuteness": 28, "Banana Affinity": 35,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/gorilla-goliath.jpg"
    },
    "ORANGUTAN OUTLAW": {
        "Strength": 83, "Agility": 80, "Intelligence": 90, "Volume": 72,
        "Cuteness": 48, "Banana Affinity": 92,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/orangutan-outlaw.jpg"
    },
    "SNOWMONKEY SHREDDER": {
        "Strength": 78, "Agility": 85, "Intelligence": 80, "Volume": 55,
        "Cuteness": 65, "Banana Affinity": 60,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/snowmonkey-shredder.jpg"
    },
    "BABOON BERSERKER": {
        "Strength": 89, "Agility": 75, "Intelligence": 68, "Volume": 82,
        "Cuteness": 30, "Banana Affinity": 72,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/baboon-berserker.jpg"
    },
    "HOWLER MONKEY HOWITZER": {
        "Strength": 80, "Agility": 82, "Intelligence": 85, "Volume": 95,
        "Cuteness": 45, "Banana Affinity": 68,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/howler-monkey-howitzer.jpg"
    },
    "GOLDEN TAMARIN TITAN": {
        "Strength": 65, "Agility": 96, "Intelligence": 88, "Volume": 60,
        "Cuteness": 70, "Banana Affinity": 82,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/golden-tamarin-titan.jpg"
    },
    "PROBOSCIS PUNISHER": {
        "Strength": 84, "Agility": 77, "Intelligence": 79, "Volume": 90,
        "Cuteness": 42, "Banana Affinity": 65,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/proboscis-punisher.jpg"
    },
    "SQUIRREL MONKEY STRIKER": {
        "Strength": 68, "Agility": 97, "Intelligence": 86, "Volume": 75,
        "Cuteness": 68, "Banana Affinity": 80,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/squirrel-monkey-striker.jpg"
    },
    "GIBBON GLADIATOR": {
        "Strength": 76, "Agility": 94, "Intelligence": 83, "Volume": 70,
        "Cuteness": 55, "Banana Affinity": 78,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/gibbon-gladiator.jpg"
    },
    "MACAQUE MAULER": {
        "Strength": 82, "Agility": 81, "Intelligence": 84, "Volume": 67,
        "Cuteness": 52, "Banana Affinity": 73,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/macaque-mauler.jpg"
    },
    "COLOBUS CRUSHER": {
        "Strength": 74, "Agility": 89, "Intelligence": 81, "Volume": 64,
        "Cuteness": 58, "Banana Affinity": 69,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/colobus-crusher.jpg"
    },
    "BONOBO BRAWLER": {
        "Strength": 81, "Agility": 86, "Intelligence": 91, "Volume": 73,
        "Cuteness": 48, "Banana Affinity": 83,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/bonobo-brawler.jpg"
    },
    "UAKARI UPPERCUT": {
        "Strength": 79, "Agility": 84, "Intelligence": 77, "Volume": 85,
        "Cuteness": 40, "Banana Affinity": 67,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/uakari-uppercut.jpg"
    },
    "WOOLLY WARLORD": {
        "Strength": 87, "Agility": 70, "Intelligence": 76, "Volume": 78,
        "Cuteness": 45, "Banana Affinity": 74,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/woolly-warlord.jpg"
    },
    "PYGMY POWERHOUSE": {
        "Strength": 69, "Agility": 98, "Intelligence": 85, "Volume": 62,
        "Cuteness": 72, "Banana Affinity": 88,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/pygmy-powerhouse.jpg"
    },
    "LANGUR LEGIONNAIRE": {
        "Strength": 83, "Agility": 82, "Intelligence": 89, "Volume": 68,
        "Cuteness": 50, "Banana Affinity": 71,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/langur-legionnaire.jpg"
    },
    "VERVET VANGUARD": {
        "Strength": 77, "Agility": 90, "Intelligence": 87, "Volume": 66,
        "Cuteness": 55, "Banana Affinity": 76,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/vervet-vanguard.jpg"
    },
    "$GAINZ APEX": {
        "Strength": 93, "Agility": 71, "Intelligence": 80, "Volume": 85,
        "Cuteness": 28, "Banana Affinity": 84,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/gainz-apex.jpg"
    },
    "ORANGUTAN OVERLORD": {
        "Strength": 88, "Agility": 75, "Intelligence": 85, "Volume": 80,
        "Cuteness": 40, "Banana Affinity": 90,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/orangutan-overlord.jpg"
    },
    "PENDANT PRIMATE": {
        "Strength": 90, "Agility": 73, "Intelligence": 82, "Volume": 82,
        "Cuteness": 32, "Banana Affinity": 79,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/pendant-primate.jpg"
    },
    "DIAMOND ORANG": {
        "Strength": 89, "Agility": 74, "Intelligence": 86, "Volume": 82,
        "Cuteness": 38, "Banana Affinity": 88,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/diamond-orang.jpg"
    },
    "LUXURY PRIMATE": {
        "Strength": 91, "Agility": 72, "Intelligence": 81, "Volume": 84,
        "Cuteness": 30, "Banana Affinity": 82,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/luxury-primate.jpg"
    },
    "CHROME GORILLA": {
        "Strength": 96, "Agility": 67, "Intelligence": 76, "Volume": 88,
        "Cuteness": 22, "Banana Affinity": 81,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/chrome-gorilla.jpg"
    },
    "GOLD TITAN APE": {
        "Strength": 94, "Agility": 70, "Intelligence": 78, "Volume": 85,
        "Cuteness": 24, "Banana Affinity": 82,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/gold-titan-ape.jpg"
    },
    "MIRROR BACK GORILLA": {
        "Strength": 95, "Agility": 68, "Intelligence": 75, "Volume": 87,
        "Cuteness": 21, "Banana Affinity": 80,
        "image": "https://github.com/MonkeyMuscle121/gainz-battles-bot/blob/main/cards/mirror-back-gorilla.jpg"
    }
}

def get_random_card():
    name = random.choice(list(MONKEY_CARDS.keys()))
    return name, MONKEY_CARDS[name].copy()

def get_all_cards():
    return MONKEY_CARDS
