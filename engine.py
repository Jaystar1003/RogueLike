import item_types
import main
import npc_types
import obstacle_types
import ui
import random as r


obstacle_coordinates = []
items_coordinates = []
directions_list = [(1, 0), (-1, 0), (0, 1), (0, -1)]
armor_list = []
weapon_list = []

villager_quotes = ["There is a legend about a dragon deep in the cave nearby...",
                   "Press 'I' to access your inventory.",
                   "The King has a task for you!",
                   "There are monsters in the forest nearby...",
                   "Collecting food will increase your health.",
                   "Greetings, traveler...",
                   "One of the villagers knows of a code...",
                   "The code is secret",
                   "Press 'Q' to quit the game."]

level_names = ["THE VILLAGE",
               "LEVEL 1: THE FOREST",
               "LEVEL 2: THE CAVE",
               "LEVEL 3: THE DRAGON'S DEN"
               ]


LEVEL = 0
npc_hp = 0
number_of_weapons = 0
number_of_armor = 0
level_1_exp = 300
level_2_exp = 600
spoken_to_king = False
win_game = False


def create_board(width, height, board_config):
    init_board = []
    for row in range(height + 1):
        init_board.append([])
        for cell in range(width + 1):
            init_board[row].append({
                "player": None,
                "npc": None,
                "item": None,
                "obstacle": None
            })

    put_obstacles_on_board(board_config, init_board, LEVEL)
    put_items_on_board(board_config, init_board, LEVEL)
    put_npc_on_board(board_config, init_board, LEVEL)

    return init_board


def put_obstacles_on_board(board_config, init_board, level):
    for config in board_config:
        print(config)

        if config['category'] == "obstacle" and config["level"] == level:

            type_of_obstacle = None

            for obstacle_type in obstacle_types.obstacle_type:
                if obstacle_type['type'] == config['type']:
                    type_of_obstacle = obstacle_type

            for i in range(config['amount']):
                first_coordinate = r.randint(0, 19)
                second_coordinate = r.randint(0, 29)
                obstacle_coordinates.append((first_coordinate, second_coordinate))
                init_board[first_coordinate][second_coordinate]['obstacle'] = type_of_obstacle


def put_items_on_board(board_config, init_board, level):
    for config in board_config:

        if config['category'] == "item" and config["level"] == level:

            type_of_item = None

            for item_type in item_types.item_type:
                if item_type['type'] == config['type']:
                    type_of_item = item_type

            for i in range(config['amount']):
                first_coordinate = r.randint(0, 19)
                second_coordinate = r.randint(0, 29)
                while (first_coordinate, second_coordinate) in obstacle_coordinates:
                    first_coordinate = r.randint(0, 19)
                    second_coordinate = r.randint(0, 29)
                items_coordinates.append((first_coordinate, second_coordinate))
                init_board[first_coordinate][second_coordinate]['item'] = type_of_item


def put_npc_on_board(board_config, init_board, level):
    for config in board_config:
        if config['category'] == "npc" and config["level"] == level:
            type_of_npc = None

            for npc_type in npc_types.npc_type:
                if npc_type['type'] == config['type']:
                    type_of_npc = npc_type

            for i in range(config['amount']):
                first_coordinate = r.randint(0, 19)
                second_coordinate = r.randint(0, 29)
                while (first_coordinate, second_coordinate) in items_coordinates:
                    first_coordinate = r.randint(0, 19)
                    second_coordinate = r.randint(0, 29)
                init_board[first_coordinate][second_coordinate]['npc'] = type_of_npc


def put_player_on_board(board, player):
    board[player['height']][player['width']]['player'] = player


def remove_from_board(board_config, init_board, height, width):
    for config in board_config:
        if config['category'] == "obstacle" or "npc" or "item":
            for i in range(height + 1):
                for j in range(width + 1):
                    if config['category'] == "obstacle":
                        init_board[i][j]['obstacle'] = None
                    elif config['category'] == "npc":
                        init_board[i][j]['npc'] = None
                    elif config['category'] == "item":
                        init_board[i][j]['item'] = None


def move_player(key, player, board):
    global npc_hp, LEVEL, spoken_to_king, win_game
    actual_height = player['height']
    actual_width = player['width']

    max_row_index = len(board) + 1
    max_column_index = len(board[0]) + 1

    new_height, new_width = get_new_position(actual_height, actual_width, key)

    try:
        if not board[new_height][new_width]['obstacle']:

            if max_row_index >= new_height >= 0 and max_column_index >= new_width >= 0:
                player['width'] = new_width
                player['height'] = new_height

                board[actual_height][actual_width]['player'] = None
                board[new_height][new_width]['player'] = player

                if board[new_height][new_width]['item']:
                    handle_item_action(board, new_height, new_width, player)

        if board[new_height][new_width]['npc']:
            npc = board[new_height][new_width]['npc']
            if npc['class'] == 'monster':
                if npc_hp == 0:
                    npc_hp = npc['hp']
                npc['hp'] -= player['damage']
                player['hp'] -= (npc['damage'] - player['armor'] * 0.01)
                player['hp'] = round(player['hp'], 2)
                ui.LOG = f"{npc['type']} HP: {npc['hp']}"
                if npc['hp'] <= 0:
                    if npc['type'] == 'dragon':
                        board[new_height][new_width]['npc'] = npc_types.npc_type[5]
                    else:
                        board[new_height][new_width]['npc'] = None
                        board[new_height][new_width]['item'] = item_types.item_type[-1]
                    npc['hp'] = npc_hp
                    player['exp'] += npc['exp']
                    ui.LOG = f"You win! {npc['exp']} EXP gained!"
            elif npc['type'] == 'king' and LEVEL == 0:
                ui.LOG = "KING: Greetings traveller, find the keys; use them to find and kill the dragon!"
                spoken_to_king = True
            elif npc['type'] == "man" or "woman":
                ui.LOG = f"{str(npc['type']).upper()}: {r.choice(villager_quotes)}"
            if npc['type'] == 'king' and LEVEL == 3:
                ui.LOG = "KING: Congratulations traveller! Thank you for playing our little game!"
                win_game = True

        import board_config

        if (new_height, new_width) == (ui.gates_list[0] - 1, 0) and LEVEL == 0 \
                and spoken_to_king is True:
            next_level("LEVEL 1: THE FOREST", board_config.starter_board, board_config.first_board, board)
        elif (new_height, new_width) == (ui.gates_list[0] - 1, 0) and LEVEL == 0 \
                and spoken_to_king is False:
            ui.LOG = "I should speak to someone first. The King spoke of a legend..."

        if (new_height, new_width) == (ui.gates_list[1] - 1, 30) and LEVEL == 1 \
                and player['keys'] >= 1 and player['exp'] >= level_1_exp:
            next_level("LEVEL 2: THE CAVE", board_config.first_board, board_config.second_board, board)
        elif (new_height, new_width) == (ui.gates_list[1] - 1, 30) and LEVEL == 1 \
                and player['keys'] < 1 and player['exp'] >= level_1_exp:
            ui.LOG = "It's locked! I need to find a key!"
        elif (new_height, new_width) == (ui.gates_list[1] - 1, 30) and LEVEL == 1 \
                and player['keys'] >= 1 and player['exp'] < level_1_exp:
            ui.LOG = "Not enough EXP... I need to kill more monsters!"
        elif (new_height, new_width) == (ui.gates_list[1] - 1, 30) and LEVEL == 1 \
                and player['keys'] < 1 and player['exp'] < level_1_exp:
            ui.LOG = "What a strange gate... I should explore this place first!"

        if (new_height, new_width) == (ui.gates_list[2] - 1, 0) and LEVEL == 2 \
                and player['keys'] >= 2 and player['exp'] >= level_2_exp:
            next_level("LEVEL 3: THE DRAGON'S DEN", board_config.second_board, board_config.third_board, board)
        elif (new_height, new_width) == (ui.gates_list[2] - 1, 0) and LEVEL == 2 \
                and player['keys'] < 2 and player['exp'] >= level_2_exp:
            ui.LOG = "It's locked! I need to find a key!"
        elif (new_height, new_width) == (ui.gates_list[2] - 1, 0) and LEVEL == 2 \
                and player['keys'] >= 2 and player['exp'] < level_2_exp:
            ui.LOG = "Not enough EXP... I need to kill more monsters!"
        elif (new_height, new_width) == (ui.gates_list[2] - 1, 0) and LEVEL == 2 \
                and player['keys'] < 2 and player['exp'] < level_2_exp:
            ui.LOG = "What a strange gate... I should explore this place first!"

        else:
            pass

    except IndexError:
        pass


def next_level(log, board_config_from, board_config_to, board):
    global LEVEL
    LEVEL += 1
    ui.LOG = log
    remove_from_board(board_config_from, board, main.BOARD_HEIGHT, main.BOARD_WIDTH)
    put_obstacles_on_board(board_config_to, board, LEVEL)
    put_items_on_board(board_config_to, board, LEVEL)
    put_npc_on_board(board_config_to, board, LEVEL)


def move_npc(board, board_config, height, width):
    for config in board_config:
        if config['category'] == "npc":
            npc_direction = r.choice(directions_list)
            for npc_height in range(height + 1):
                for npc_width in range(width + 1):
                    npc_save = board[npc_height][npc_width]['npc']
                    board[npc_height][npc_width]['npc'] = None
                    npc_height += npc_direction[0]
                    npc_width += npc_direction[1]
                    while board[npc_height][npc_width]['npc'] or board[npc_height][npc_width]['item'] \
                            or board[npc_height][npc_width]['obstacle'] \
                            or npc_height < 0 or npc_height > height or npc_width < 0 or npc_width > width:
                        npc_height -= npc_direction[0]
                        npc_width -= npc_direction[1]
                        npc_direction = r.choice(directions_list)
                        npc_height += npc_direction[0]
                        npc_width += npc_direction[1]
                    board[npc_height][npc_width]['npc'] = npc_save
                    npc_height -= npc_direction[0]
                    npc_width -= npc_direction[1]


def get_new_position(actual_height, actual_width, key):
    if key == 'W':
        new_height = actual_height - 1
        new_width = actual_width
    elif key == 'A':
        new_height = actual_height
        new_width = actual_width - 1
    elif key == 'S':
        new_height = actual_height + 1
        new_width = actual_width
    elif key == 'D':
        new_height = actual_height
        new_width = actual_width + 1
    else:
        raise Exception(f"Key not supported for player movement. Pressed [{key}]")
    return new_height, new_width


def handle_item_action(board, new_height, new_width, player):
    global number_of_weapons, number_of_armor
    item = board[new_height][new_width]['item']
    if item and item['class'] == 'money':
        player['cash'] += item['value']
        board[new_height][new_width]['item'] = None
        ui.LOG = f"+ {item['value']} gold"
    elif item and item['class'] == 'key':
        player['keys'] += 1
        board[new_height][new_width]['item'] = None
        ui.LOG = "+ 1 key"
    elif item and item['class'] == 'weapon':
        player['damage'] += item['damage']
        if item['type'] not in weapon_list:
            weapon_list.append(item['type'])
        number_of_weapons += 1
        board[new_height][new_width]['item'] = None
        ui.LOG = f"{item['type']} added to inventory. | + {item['damage']} damage"
    elif item and item['class'] == 'armor':
        player['armor'] += item['defence']
        if item['type'] not in armor_list:
            armor_list.append(item['type'])
        number_of_armor += 1
        board[new_height][new_width]['item'] = None
        ui.LOG = f"{item['type']} added to inventory. | + {item['defence']} defence"
    elif item and item['class'] == 'food':
        player['hp'] += item['hp']
        board[new_height][new_width]['item'] = None
        ui.LOG = f"Delicious! | + {item['hp']} HP"
    elif item and item['class'] == 'sign':
        ui.LOG = input(f"I can write something here...\n >>> ")
        if ui.LOG == "secret":
            for elt in npc_types.npc_type:
                if elt['type'] == 'dragon':
                    elt['hp'] = 200
                    ui.LOG = "You hear a loud screech of pain in the distance..."
        else:
            ui.LOG = "Nothing happened..."
