import util
import engine
import ui
import player_types
import board_config
import time

PLAYER_START_X = 3
PLAYER_START_Y = 3

BOARD_WIDTH = 30
BOARD_HEIGHT = 20

player = None


def create_player():
    global player
    print(f"{ui.Colors.UNDERLINE}Choose your race:{ui.Colors.END}\n")
    for player_type in player_types.types:
        print(f"{player_type['id']}: {player_type['race']}")

    player_chosen_type_id = 0
    while player_chosen_type_id not in (1, 2):
        player_chosen_type_id = int(input("\nPlease enter 1 or 2  >>> "))
    player_name = input("\nWhat's your name >>> ")

    player_chosen_type = None

    for player_type in player_types.types:
        if player_type['id'] == player_chosen_type_id:
            player_chosen_type = player_type
            break

    player = player_types.get_init_player(player_chosen_type, player_name)

    return player


def main():
    global player
    start_screen()

    player = create_player()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT, board_config.starter_board)

    util.clear_screen()
    is_running = True
    engine.put_player_on_board(board, player)

    while is_running:
        ui.display_board(board, player)
        key = util.key_pressed()

        if key.lower() == 'q':
            is_running = False
        elif key.upper() in "WASD":
            engine.move_player(key.upper(), player, board)
            try:
                if engine.LEVEL == 0:
                    engine.move_npc(board, board_config.starter_board, BOARD_HEIGHT, BOARD_WIDTH)
                elif engine.LEVEL == 1:
                    engine.move_npc(board, board_config.first_board, BOARD_HEIGHT, BOARD_WIDTH)
                elif engine.LEVEL == 2:
                    engine.move_npc(board, board_config.second_board, BOARD_HEIGHT, BOARD_WIDTH)
                elif engine.LEVEL == 3:
                    engine.move_npc(board, board_config.third_board, BOARD_HEIGHT, BOARD_WIDTH)
            except IndexError:
                pass
        elif key.upper() == "I":
            util.clear_screen()
            ui.display_inventory(player)
            time.sleep(2.5)
        if player['hp'] <= 0:
            game_over()
            time.sleep(5)
            is_running = False
        if engine.win_game is True:
            ui.display_board(board, player)
            time.sleep(3)
            you_win()
            time.sleep(5)
            is_running = False
        else:
            pass

        util.clear_screen()


def start_screen():
    print(f"""\
        {ui.Colors.Magenta}{ui.Colors.BOLD}
     ______    _______  _______  __   __  _______    ___      ___   ___   _  _______   
    |    _ |  |       ||       ||  | |  ||       |  |   |    |   | |   | | ||       |  
    |   | ||  |   _   ||    ___||  | |  ||    ___|  |   |    |   | |   |_| ||    ___|  
    |   |_||_ |  | |  ||   | __ |  |_|  ||   |___   |   |    |   | |      _||   |___   
    |    __  ||  |_|  ||   ||  ||       ||    ___|  |   |___ |   | |     |_ |    ___|  
    |   |  | ||       ||   |_| ||       ||   |___   |       ||   | |    _  ||   |___   
    |___|  |_||_______||_______||_______||_______|  |_______||___| |___| |_||_______|  
                           _______  _______  __   __  _______                          
                          |       ||   _   ||  |_|  ||       |                         
                          |    ___||  |_|  ||       ||    ___|                         
                          |   | __ |       ||       ||   |___                          
                          |   ||  ||       ||       ||    ___|                         
                          |   |_| ||   _   || ||_|| ||   |___                          
                          |_______||__| |__||_|   |_||_______|                         
        {ui.Colors.END}
        \n\n\n""")


def game_over():
    print(f"""\
    {ui.Colors.Red}{ui.Colors.BOLD}\n\n\n\n                 
     _______  _______  __   __  _______    _______  __   __  _______  ______   
    |       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  
    |    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  
    |   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ 
    |   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |
    |   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |
    |_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|
                {ui.Colors.END}\n\n\n\n 
                """)
    print("Game will automatically end in 5 seconds...")


def you_win():
    print(f"""\
    {ui.Colors.Magenta}{ui.Colors.BOLD}\n\n\n\n
    :::   :::  ::::::::  :::    :::       :::       ::: ::::::::::: ::::    ::: 
    :+:   :+: :+:    :+: :+:    :+:       :+:       :+:     :+:     :+:+:   :+: 
     +:+ +:+  +:+    +:+ +:+    +:+       +:+       +:+     +:+     :+:+:+  +:+ 
      +#++:   +#+    +:+ +#+    +:+       +#+  +:+  +#+     +#+     +#+ +:+ +#+ 
       +#+    +#+    +#+ +#+    +#+       +#+ +#+#+ +#+     +#+     +#+  +#+#+# 
       #+#    #+#    #+# #+#    #+#        #+#+# #+#+#      #+#     #+#   #+#+# 
       ###     ########   ########          ###   ###   ########### ###    #### 
                                {ui.Colors.END}    
                """)
    print(f"""\
                {ui.Colors.BOLD}{ui.Colors.Blue}
                                  CREATED BY:
                                ---------------
                                  JAKUB ZAJĄC
                                 GABRIEL KYZIOŁ
                                JAKUB ROMANOWSKI
                                  DANIEL KOSK
                              KRZYSZTOF WIŚNIEWSKI

                              ---------------------
                              Thank you for playing!
                    {ui.Colors.END}            
                """)


if __name__ == '__main__':
    main()
