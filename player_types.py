types = [
    {
        "race": "Elf",
        "armor": 100,
        "damage": 20,
        "hp": 200,
        "exp": 0,
        "cash": 0,
        "id": 1,
        "icon": "🧝"
    },
    {
        "race": "Mage",
        "armor": 150,
        "damage": 25,
        "hp": 150,
        "exp": 0,
        "cash": 0,
        "id": 2,
        "icon": "🧙"
    }
]


def get_init_player(player_chosen_type, player_name):
    player = {
        "name": player_name,
        "hp": player_chosen_type['hp'],
        "armor": player_chosen_type['armor'],
        "damage": player_chosen_type['damage'],
        "race": player_chosen_type['race'],
        "exp": 0,
        "cash": 5,
        "visual": player_chosen_type['icon'],
        "height": 3,
        "width": 3,
        "keys": 0
    }
    return player
