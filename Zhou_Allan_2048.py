"""This program runs the popular game, 2048, and contains all of its graphic 
and game logic functions for a terminal-based setting with keyboard 
characters.

The program also has a game settings option, which can be used to change or
create keybinds for the game, based on user preference.

Constants in the program can be edited to play 2048 on a differently sized 
game board. However, the game will by default be played on a 4 by 4 grid.
"""


__author__ = "Allan Zhou"


from random import randint 
from random import random
from time import sleep


# Graphics Constants
TIME_DELAY = 3
TILE_LENGTH = 6
BOARD_SIDE_LENGTH = 4
GAME_BOARD_WIDTH = TILE_LENGTH * BOARD_SIDE_LENGTH + 3

# Program Choice Constants
PLAY = "1"
QUIT = "2"
SETTINGS = "3"
VALID_GAME_CHOICES = [PLAY, QUIT, SETTINGS]

# Tile Constants
STARTING_TILES = 2
TILE_BASE = 2
WINNING_TILE = 2048
EMPTY_TILE = 0
MAX_TILE = 2 ** 20
TILE_CHANCE_4 = 0.9

# Keyboard Binding Constants 
MOVES_WASD = {"up": "w",
              "left": "a",
              "down": "s",
              "right": "d", 
              "quit" : "q"}

MOVES_ESDF = {"up": "e",
              "left": "s",
              "down": "d",
              "right": "f", 
              "quit": "q"}


def choose_key_bind(key_bind_mode: dict) -> dict: 
    """Return the user's choice for the keybinding used to perform moves 
    during a round of 2048 as a dictionary. Users have the option to create 
    their own custom keybind."""

    print("\nCurrent Keybinds: ")
    print_key_bind(key_bind_mode)

    # List the possible key bind options.
    print("1. w (up) a (left) s (down) d (right) q (quit) Default Bind.")
    print("2. e (up) s (left) d (down) f (right) q (quit) Bind.")
    print("3. Custom Bind.\n")

    while True:
        key_bind = input("Choose Keybind: ")

        if key_bind in VALID_GAME_CHOICES:
            if key_bind == "1":
                key_bind_mode = MOVES_WASD

            elif key_bind == "2":
                key_bind_mode = MOVES_ESDF

            elif key_bind == "3":
                # Set up a new dictionary for key binding. 
                key_bind_mode = {"up": None,
                                 "left": None,
                                 "down": None,
                                 "right": None, 
                                 "quit": None}

                # Prompt user for new key binds for the 5 possible moves.
                print()
                for key in key_bind_mode:
                    new_value = input("Your key for the move {}: "
                                    .format(key)).strip()
                    key_bind_mode[key] = new_value

            print("\nUsing key binding: ")
            print_key_bind(key_bind_mode)
                
            return key_bind_mode

        else:
            print("Invalid keybind choice. Please try again.\n")


def print_key_bind(key_bind_mode: dict): 
    """Print the key-value pairs in key_bind_mode. The key-value pairs in 
    the dictionary key_bind_mode link specific keys to moves in the game."""

    for key in key_bind_mode: 
        print("{} : {}".format(key, key_bind_mode[key]))

    print()


def print_board(game_tiles: list):
    """Print the game board, using the tile numbers in the two dimensional
    list, game_tiles."""

    for row in range(BOARD_SIDE_LENGTH):
        # Top horizontal line with corners.
        if row == 0:
            print("╔", end = "")
            for i in range(BOARD_SIDE_LENGTH):
                # End of the top horizontal line will have a corner.
                if i == BOARD_SIDE_LENGTH - 1: 
                    print("═" * TILE_LENGTH + "╗")
                else: 
                    print("═" * TILE_LENGTH + "╦", end="")

        # Middle horizontal lines with edges.
        else:
            print("╠", end = "")
            for i in range(BOARD_SIDE_LENGTH): 
                # End of the middle horizontal line will have a row connector.
                if i == BOARD_SIDE_LENGTH - 1: 
                    print("═" * TILE_LENGTH + "╣")
                else: 
                    print("═" * TILE_LENGTH + "╬", end="")

        # Begin a row of number tiles.
        print("║", end="")

        # Print tiles in columns, separated by vertical lines. 
        for column in range(BOARD_SIDE_LENGTH):
            tile = game_tiles[row][column]
            # Tiles with the value of 0 will be printed with empty spaces.
            if tile != 0:
                print("{:>{width}}║".format(game_tiles[row][column],
                    width=TILE_LENGTH), end="")
            else: 
                print(" " * TILE_LENGTH + "║", end="")

        print()

    # Bottom horizontal line with corners.
    print("╚", end = "")
    for i in range(BOARD_SIDE_LENGTH): 
        # End of bottom horziontal line will have a corner.
        if i == BOARD_SIDE_LENGTH - 1: 
            print("═" * TILE_LENGTH + "╝")
        else:
            print("═" * TILE_LENGTH + "╩", end="")


def get_user_choice(won: bool) -> str:
    """Prompt the user to enter a game choice, which corresponds to play, 
    quit, and game settings. Return the valid choice as a string. If won is 
    True, give option to continue the game instead of playing the game."""

    while True:
        if won:
            print("1. Continue Game.\n2. Exit Game.\n3. Game Settings.\n")
        else:
            print("Main Menu\n" + "═" * len("Main Menu"))
            print("1. Play Game. \n2. Quit 2048.\n3. Game Settings.\n")

        choice = input("Your choice: ")

        # Ensure that user enters a valid game choice.
        if choice in VALID_GAME_CHOICES:
            return choice
        else:
            print("Invalid choice. Valid choices are " + 
            "({}) for play, ({}) for quit, and ({}) for settings.\n"
            .format(PLAY, QUIT, SETTINGS))


def get_valid_move(key_bind_mode: dict) -> str:
    """Prompt the user to enter a board move corresponding to up, left, down, 
    right, or quit. Return the valid move as a string."""

    while True:
        move = input("Enter a direction to move: ")
        valid_move = False 

        # Ensure the direction entered is valid.
        for key in key_bind_mode: 
            if key_bind_mode[key] == move:
                valid_move = True
                break

        if valid_move:
            return move
        
        print("\nValid moves are {}, {}, {}, {}, and {}. " 
            .format(key_bind_mode["up"], key_bind_mode["left"], 
            key_bind_mode["down"], key_bind_mode["right"], 
            key_bind_mode["quit"]) + "Please try again.\n")


def generate_empty_board() -> list:
    """Generates a empty game board, which is a 4 by 4 two dimensional list
    with only 0s. 

    >>> generate_empty_board() 
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]] 
    """

    game_tiles = []

    for i in range(BOARD_SIDE_LENGTH):
        game_tiles.append([0] * BOARD_SIDE_LENGTH)

    return game_tiles


def tile_shift(game_tiles: list, upwards: bool) -> list:
    """Shift the tiles in the grid game_tiles in the upwards or leftwards 
    direction, based on the boolean upwards. Return the new game tiles as 
    a two dimensional list. 

    >>> tile_shift([[0, 0, 0, 0],
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 2]], True) 
    [[0, 0, 0, 2], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0]]

    >>> tile_shift([[0, 0, 0, 0],
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 2]], False) 
    [[0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [2, 0, 0, 0]]
    """

    shifted_tiles = generate_empty_board()

    # Tile shift upwards.
    if upwards:
        for col in range(BOARD_SIDE_LENGTH):
            empty_position = 0

            for row in range(BOARD_SIDE_LENGTH):
                # Shift non-zero tiles as far up as possible (no merge).
                if game_tiles[row][col] != 0:
                    shifted_tiles[empty_position][col] = game_tiles[row][col]
                    empty_position += 1

    # Tile shift leftwards.
    else:
        for row in range(BOARD_SIDE_LENGTH):
            empty_position = 0

            for col in range(BOARD_SIDE_LENGTH):
                # Shift non-zero tiles as far left as possible (no merge).
                if game_tiles[row][col] != 0:
                    shifted_tiles[row][empty_position] = game_tiles[row][col]
                    empty_position += 1

    return shifted_tiles


def reflect_game_board(game_tiles: list, vertical: bool) -> list:
    """Reflect the tiles in the grid game_tiles vertically or horizontally, 
    depending on the boolean vertical. Return the new game tiles as a two 
    dimensional list. 

    >>> reflect_game_board([[0, 0, 2, 2], 
                            [0, 0, 0, 4], 
                            [0, 0, 0, 8], 
                            [0, 2, 0, 2]], False) 
    [[2, 2, 0, 0], 
     [4, 0, 0, 0], 
     [8, 0, 0, 0], 
     [2, 0, 2, 0]]

    >>> reflect_game_board([[0, 0, 2, 2], 
                            [0, 0, 0, 4], 
                            [0, 0, 0, 8], 
                            [0, 2, 0, 2]], True)
    [[0, 2, 0, 2], 
     [0, 0, 0, 8], 
     [0, 0, 0, 4], 
     [0, 0, 2, 2]]
    """

    reflected_tiles = generate_empty_board()

    # Flip game board contents over a mirror line between rows 2 and 3.
    if vertical:
        for row in range(BOARD_SIDE_LENGTH):
            reflected_tiles[row] = game_tiles[BOARD_SIDE_LENGTH - 1 - row]

    # Flip game board contents over a mirror line between columns 2 and 3.
    else:
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH):

                reflected_column = BOARD_SIDE_LENGTH - 1 - col
                reflected_tiles[row][col] = game_tiles[row][reflected_column]

    return reflected_tiles


def merge_game_board(game_tiles: list, upwards: bool) -> tuple:
    """Merge the tiles in the grid game_tiles in the upwards or leftwards 
    direction, based on the boolean direction. Return the merged game tiles 
    as a two dimensional list. 

    >>> merge_game_board([[4, 2, 2, 8], 
                          [4, 4, 0, 8], 
                          [0, 2, 0, 0], 
                          [0, 0, 0, 2]], True)
    ([[8, 2, 2, 16], 
      [0, 4, 0, 0], 
      [0, 2, 0, 0], 
      [0, 0, 0, 2]], 24)

    >>> merge_game_board([[4, 2, 2, 8], 
                          [4, 4, 0, 8], 
                          [0, 2, 0, 0], 
                          [0, 0, 0, 2]], False)
    ([[4, 4, 0, 8], 
      [8, 0, 0, 8], 
      [0, 2, 0, 0], 
      [0, 0, 0, 2]], 12)
    """

    merge_score = 0

    merged_tiles = game_tiles

    # Merge game board upwards.
    if upwards:
        for col in range(BOARD_SIDE_LENGTH):
            for row in range(BOARD_SIDE_LENGTH - 1):
                top_tile = game_tiles[row][col]
                bottom_tile = game_tiles[row + 1][col]

                # Merge two non-zero equal tiles in the same column together.
                if top_tile == bottom_tile and top_tile != 0:
                    merge_score += top_tile + bottom_tile
                    merged_tiles[row][col] = top_tile + bottom_tile
                    merged_tiles[row + 1][col] = 0

    # Merge game board leftwards.
    else:
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH - 1):
                left_tile = game_tiles[row][col]
                right_tile = game_tiles[row][col + 1]

                # Merge two non-zero equal tiles in the same row together.
                if left_tile == right_tile and left_tile != 0:
                    merge_score += left_tile + right_tile
                    merged_tiles[row][col] = left_tile + right_tile
                    merged_tiles[row][col + 1] = 0

    return merged_tiles, merge_score


def add_random_tile(game_tiles: list) -> list:
    """Add a 2 or 4 tile to the grid, game_tiles, at a random empty tile.
    There is a 90 percent chance of adding a 2 tile and a 10 percent chance 
    of adding a 4 tile. Return game_tiles after a tile is added."""

    new_tile = random() 

    if new_tile > TILE_CHANCE_4: 
        random_tile = TILE_BASE ** 2 
    else: 
        random_tile = TILE_BASE

    # Place new tile in random, empty tile spot. 
    while True:
        row = randint(0, BOARD_SIDE_LENGTH - 1)
        col = randint(0, BOARD_SIDE_LENGTH - 1)

        if game_tiles[row][col] == 0:
            game_tiles[row][col] = random_tile
            return game_tiles


def check_tile(game_tiles: list, value: int) -> bool:
    """Return True if value is in the game board, game_tiles. Otherwise, 
    return False.

    >>> check_tile([[2048, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]], 2048)
    True
    """

    for row in game_tiles:
        if value in row:
            return True

    return False


def move_up(game_tiles: list) -> tuple:
    """Perform one move of the game board, game_tiles, upwards. One move 
    upwards consists of two upwards tile shifts, with one upwards tile 
    merge in between. Return the game board after the up move and the score
    accumulated from the move.

    >>> move_up([[0, 2, 2, 8], 
                 [4, 0, 0, 8], 
                 [0, 2, 0, 0], 
                 [2, 0, 0, 2]])

    [[4, 4, 2, 16], 
     [2, 0, 0, 2], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0]]
    """

    game_tiles = tile_shift(game_tiles, True)
    game_tiles, score = merge_game_board(game_tiles, True)
    game_tiles = tile_shift(game_tiles, True)

    return game_tiles, score


def move_left(game_tiles: list) -> tuple:
    """Perform one move of the game board, game_tiles, leftwards. One move 
    leftwards consists of two tile shifts left, with one leftwards tile merge
    in between. Return the game board after the left move and the score
    accumulated from the move.

    >>> move_left([[0, 2, 2, 8], 
                   [4, 0, 0, 8], 
                   [0, 2, 0, 0], 
                   [2, 0, 0, 2]])
    ([[4, 4, 2, 16], 
      [2, 0, 0, 2], 
      [0, 0, 0, 0], 
      [0, 0, 0, 0]], 20)
    """

    game_tiles = tile_shift(game_tiles, False)
    game_tiles, score = merge_game_board(game_tiles, False)
    game_tiles = tile_shift(game_tiles, False)

    return game_tiles, score


def game_board_move(game_tiles: list, direction: str, 
                    key_bind_mode: dict) -> tuple:
    """Perform one move of the game board, in any direction (up, down, left, 
    or right). Return the game tiles after the move and the points earned from
    the move. 

    >>> game_board_move([[0, 0, 0, 2], 
                         [0, 2, 0, 0], 
                         [0, 4, 0, 0], 
                         [2, 0, 0, 0]], "w", 
                         {"up" : "w",
                          "left" : "a",
                          "down" : "s",
                          "right" : "d", 
                          "quit" : "q"})
    ([[2, 2, 0, 2], 
      [0, 4, 0, 0], 
      [0, 0, 0, 0], 
      [0, 0, 0, 0]], 0)

    >>> game_board_move([[2, 2, 0, 2], 
                         [0, 4, 0, 0], 
                         [0, 0, 0, 0], 
                         [0, 0, 0, 0]], "a", 
                         {"up" : "w",
                          "left" : "a",
                          "down" : "s",
                          "right" : "d", 
                          "quit" : "q"})
    ([[4, 2, 0, 0], 
      [4, 0, 0, 0], 
      [0, 0, 0, 0], 
      [0, 0, 0, 0]], 4)
    """

    moved_tiles = game_tiles

    if direction == key_bind_mode["up"]:
        moved_tiles, score = move_up(game_tiles)
        move_direction = "up"

    # A move downwards is a reflected move upwards.
    elif direction == key_bind_mode["down"]:
        moved_tiles = reflect_game_board(game_tiles, True)
        moved_tiles, score = move_up(moved_tiles)
        moved_tiles = reflect_game_board(moved_tiles, True)
        move_direction = "down"

    elif direction == key_bind_mode["left"]:
        moved_tiles, score = move_left(game_tiles)
        move_direction = "left"

    # A move rightwards is a reflected move leftwards.
    else:
        moved_tiles = reflect_game_board(game_tiles, False)
        moved_tiles, score = move_left(moved_tiles)
        moved_tiles = reflect_game_board(moved_tiles, False)
        move_direction = "right"

    # The game board did not change after the move was performed. 
    if moved_tiles == game_tiles:
        print("The move {}wards does not move any tiles.\n"
              .format(move_direction))

    return moved_tiles, score


def game_outcome(game_tiles: list, won: bool) -> str:
    """Return "win" if the user has won the round by creating the tile 
    2048 in game_tiles and the user has not won in a previous move. If the 
    user has not won yet, Return "in progress" if any possible moves can be 
    made in game_tiles. Otherwise, return "loss".
    
    >>> game_outcome([[0, 2, 2, 8], 
                      [4, 0, 0, 8], 
                      [0, 2, 0, 0], 
                      [2, 0, 0, 2]], False)
    "in progress" 

    >>> game_outcome([[2, 4, 2, 8], 
                      [4, 16, 32, 512], 
                      [32, 2, 128, 64], 
                      [2, 4, 1024, 2]], False)
    "loss"

    >>> game_outcome([2048, 4, 0, 8], 
                     [4, 0, 32, 512], 
                     [0, 2, 32, 0], 
                     [2, 0, 1024, 2]], True)
    "in progress"
    """

    # The user has created the winning tile for the first time.
    if check_tile(game_tiles, WINNING_TILE) and not won:
        return "win"

    # If there are empty tiles, there is a possible move.
    elif check_tile(game_tiles, EMPTY_TILE):
        return "in progress"

    # Check for mergeable tiles.
    else:
        # Is horizontal tile merging possible?
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH - 1):
                if game_tiles[row][col] == game_tiles[row][col + 1]:
                    return "in progress"

        # Is vertical tile merging possible?
        for col in range(BOARD_SIDE_LENGTH):
            for row in range(BOARD_SIDE_LENGTH - 1):
                if game_tiles[row][col] == game_tiles[row + 1][col]:
                    return "in progress"

        # No possible moves on the game board.
        return "loss"


def game_round(key_bind_mode: dict) -> int:
    """Play one single round of 2048. Return the score from the round."""

    # When two tiles are merged, the value of their sum is added to the score.
    round_score = 0
    won = False

    game_tiles = generate_empty_board()

    # Start with 2 tiles, which are either 2 or 4. 
    for i in range(STARTING_TILES):
        game_tiles = add_random_tile(game_tiles)

    print_key_bind(key_bind_mode)
    print_board(game_tiles)

    while game_outcome(game_tiles, won) != "loss":  
        # The player has created the winning tile for the first time. 
        if check_tile(game_tiles, WINNING_TILE) and not won:
            print("Hooray! You won!\n")
            won = True
            choice = get_user_choice(True)
            
            # Ensure player enters valid game choice.
            while True: 
                if choice == QUIT:
                    print("\nExiting Game...\n")
                    sleep(TIME_DELAY)
                    return round_score
                elif choice == PLAY:
                    print()
                    print_board(game_tiles)
                    break
                elif choice == SETTINGS:
                    key_bind_mode = choose_key_bind(key_bind_mode)
                    print_board(game_tiles)
                    break
                else: 
                    print("Invalid choice, please try again.")

        move = get_valid_move(key_bind_mode)
        print()
        
        # User decides to quit in the middle of the round.
        if move == key_bind_mode["quit"]: 
            while True: 
                choice = input("Are you sure you want to quit the current " 
                + "round? y/n: ")

                if choice == "y": 
                    print("\nQuitting Game...\n")
                    sleep(TIME_DELAY)
                    return round_score

                elif choice == "n": 
                    # Print the game board and return to top of game loop. 
                    print()
                    print_board(game_tiles)
                    break 

                else: 
                    print("\nInvalid choice, please try again.\n")
        
        else: 
            new_game_tiles, move_score = game_board_move(
                game_tiles, move, key_bind_mode)

            round_score += move_score

            # End the game when a seven digit tile has been created.
            if check_tile(game_tiles, MAX_TILE):
                print("The game has ended.\n")
                break

            # If the board does not have an empty square or the move performed did 
            # not change the game board, do not add a random tile. 
            elif check_tile(new_game_tiles, EMPTY_TILE) and \
                new_game_tiles != game_tiles:

                game_tiles = add_random_tile(new_game_tiles)
            
            print_board(new_game_tiles)

    if not won: 
        print("Sorry, you lost the game. Better luck next time.\n")

    return round_score


def main():
    """The main game loop, with rules and a game overview."""

    print("Welcome to...\n")

    print("######  ######  ##  ##  ######")
    print("    ##  ##  ##  ##  ##  ##  ##")
    print("######  ##  ##  ######  ######")
    print("##      ##  ##      ##  ##  ##")
    print("######  ######      ##  ######\n")
    
    print("Overview of the Game: \n")
    print("1. The objective of the game is to create the tile 2048 by merging"
          + "\ntiles together on a 4 by 4 grid.")
    print("2. You can shift the tiles on the game board in 4 directions:"
          + "\nup, down, right, and left. When tiles are shifted, they will"
          + "\ngo as far as they can within their respective column/row.")
    print("3. During a tile shift, if two tiles of the same number collide"
          + "\nwith each other, they will merge together into one tile that"
          + "\nhas the sum of the two tiles.")
    print("4. After every move that changes the location of at least one tile" 
          + ",\na 2 or 4 tile while be added to a random, empty tile spot.")
    print("5. You lose when there are no more empty tiles and no more"
          + "\npossible moves.\n") 

    high_score = 0
    program = PLAY
    key_bind_mode = MOVES_WASD

    while program != QUIT:
        program = get_user_choice(False)

        if program == PLAY:
            # Run a single round of 2048. 
            print("\nGame starting...\n")
            sleep(TIME_DELAY)
            round_score = game_round(key_bind_mode)

            print("Total Score: {}\n".format(round_score))

            if round_score > high_score: 
                high_score = round_score

        elif program == QUIT:
            if high_score != 0:
                print("\nYour highest score was {}.".format(high_score))

            print("\nThanks for playing 2048. Goodbye!")

        elif program == SETTINGS: 
            key_bind_mode = choose_key_bind(key_bind_mode)

        else:
            print("Invalid menu choice. Please try again.")


if __name__ == "__main__":
    main()
