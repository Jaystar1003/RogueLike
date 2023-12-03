import engine
import random as r


class Colors:
    Default = "\033[39m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


gates_list = []

for i in range(3):
    gates_list.append(r.randint(1, 18))

dialogue_height = 12
name_height = 2
hp_height = 3
exp_height = 4
armor_height = 5
damage_height = 6
cash_height = 7

LOG = "THE VILLAGE"


def display_board(board, player, gate_0=0, gate_1=0, gate_2=0):
    global LOG
    if engine.LEVEL == 0:
        board_terrain(board, gate_0, gates_list[0], 1, 0, "🌾", "  ", "", "🟫", player)

    elif engine.LEVEL == 1:
        board_terrain(board, gate_0, gates_list[0], gate_1, gates_list[1], "🌳", "  ", "🚪", "🟩", player)

    elif engine.LEVEL == 2:
        board_terrain(board, gate_2, gates_list[2], gate_1, gates_list[1], "🪨", "⛩ ", "🚪", "⬛️", player)

    elif engine.LEVEL == 3:
        board_terrain(board, gate_2, gates_list[2], 1, 0, "🔥", "⛩ ", "", "🟥", player)


def display_inventory(player):
    cash = f"{player['cash']} {(19 - len(str(player['cash']))) * ' '}|."
    keys = f"{player['keys']} {(19 - len(str(player['keys']))) * ' '}|."
    try:
        weapons = f"{engine.number_of_weapons} X {engine.weapon_list[0]} " \
                  f"{(16 - len(f'{engine.number_of_weapons} X {engine.weapon_list[0]}')) * ' '}|."
    except IndexError:
        weapons = f"- {15 * ' '}|."
    try:
        armor = f"{engine.number_of_armor} X {engine.armor_list[0]} " \
                  f"{(18 - len(f'{engine.number_of_armor} X {engine.armor_list[0]}')) * ' '}|."
    except IndexError:
        armor = f"- {17 * ' '}|."

    if engine.LEVEL == 0:
        experience = f" - "
    elif engine.LEVEL == 1:
        experience = engine.level_1_exp
    elif engine.LEVEL == 2:
        experience = engine.level_2_exp
    else:
        experience = f" ∞ "

    print(f"""\
{Colors.LightYellow}
   ______________________________
 / \                             \.
|   |       ~  {Colors.UNDERLINE}INVENTORY{Colors.END}{Colors.LightYellow}  ~      |.
 \_ |                            |.
    |                            |.
    |  Cash: {cash}              
    |  Keys: {keys}                   
    |  Weapons: {weapons}                
    |  Armor: {armor}                  
    |                            |.
    |                            |.
    | -------------------------  |.
    | Level: {engine.LEVEL}                   |.
    | Exp for next level: {experience}    |.
    |                            |.
    | Press 'Q' to quit the game |.
    |   _________________________|___
    |  /                            /.
    \_/____________________________/.
    {Colors.Default}
    """)


def dialogue_field(info):
    print(f"     ~~~   {info}   ~~~")


def board_terrain(board, gate1, gate1_place, gate2, gate2_place, emote_wall,
                  emote_gate1, emote_gate2, emote_floor, player):
    print(emote_wall * (len(board[0]) + 2))

    for row in board:
        gate1 += 1
        gate2 += 1
        if gate1 == gate1_place:
            print(emote_gate1, end='')
        else:
            print(emote_wall, end='')

        for cell in row:
            if cell['player']:
                print(cell['player']['visual'], end='')
            elif cell['item']:
                print(cell['item']['visual'], end='')
            elif cell['npc']:
                print(cell['npc']['visual'], end='')
            elif cell['obstacle']:
                print(cell['obstacle']['visual'], end='')
            else:
                print(emote_floor, end='')
        if gate2 == gate2_place:
            print(emote_gate2)
        elif gate2 == dialogue_height:
            print(emote_wall, end='')
            dialogue_field(LOG)
        elif gate2 == name_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  NAME: {player['name']}{Colors.Default}")
        elif gate2 == hp_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  HP: {player['hp']}{Colors.Default}")
        elif gate2 == exp_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  EXP: {player['exp']}{Colors.Default}")
        elif gate2 == armor_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  ARMOR: {player['armor']}{Colors.Default}")
        elif gate2 == damage_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  DAMAGE: {player['damage']}{Colors.Default}")
        elif gate2 == cash_height:
            print(emote_wall, end='')
            print(f"{Colors.Green}  CASH: {player['cash']}{Colors.Default}")
        else:
            print(emote_wall)

    print(emote_wall * (len(board[0]) + 2))
