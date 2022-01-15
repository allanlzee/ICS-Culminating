"""This program runs the popular game, 2048, and contains all of its graphic 
and game logic functions for a terminal-based setting with keyboard 
characters.

The program also has a game settings option, which can be used to change or
create keybinds for the game, based on user preference.
"""


__author__ = "Allan Zhou"


from random import randint
from time import sleep


# Graphics Constants
TIME_DELAY = 3
TILE_LENGTH = 5
BOARD_SIDE_LENGTH = 4
GAME_BOARD_WIDTH = 23

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

# Keyboard Binding Constants 
MOVES_1 = {"up": "w",
           "left": "a",
           "down": "s",
           "right": "d"}

MOVES_2 = {"up": "e",
           "left": "s",
           "down": "d",
           "right": "f"}


def choose_key_bind(key_bind: str) -> dict: 
    """Return the user's choice for the keybinding used to perform moves in 
    different directions for 2048. Users have the option to create their own
    custom keybind."""

    # List the possible key bind options.
    print("1. w (up) a (left) s (down) d (right) Default Bind.")
    print("2. e (up) s (left) d (down) f (right) Bind.")
    print("3. Custom Bind.\n")

    while True:
        key_bind = input("Choose Keybind: ")
        print()

        if key_bind in VALID_GAME_CHOICES:
            if key_bind == "1":
                key_bind_mode = MOVES_1

            elif key_bind == "2":
                key_bind_mode = MOVES_2

            elif key_bind == "3":
                # Set up a new dictionary for key binding. 
                key_bind_mode = {"up": None,
                                 "left": None,
                                 "down": None,
                                 "right": None}

                # Prompt user for new key binds in 4 directions.
                for key in key_bind_mode:
                    new_value = input("Your key for the move {}: "
                                    .format(key)).strip()
                    key_bind_mode[key] = new_value

                print()

            print("🤏 Using key binding {}. 🤏\n".format(key_bind_mode))
                
            return key_bind_mode

        else:
            print("Invalid keybind choice. Please try again.\n")


def print_board(game_tiles: str):
    """Print the game board, using the tile numbers in the two dimensional
    list, game_tiles."""

    for row in range(BOARD_SIDE_LENGTH):
        # Top horizontal line with corners.
        if row == 0:
            print("/" + "-" * GAME_BOARD_WIDTH + "\\")
        # Middle horizontal lines with edges.
        else:
            print("|" + "-" * GAME_BOARD_WIDTH + "|")

        print("|", end="")

        # Print tiles, separated by columns.
        for column in range(BOARD_SIDE_LENGTH):
            print("{:>{width}}|".format(game_tiles[row][column],
                                        width=TILE_LENGTH), end="")
        print()

    # Bottom horizontal line with corners.
    print("\\" + "-" * GAME_BOARD_WIDTH + "/")


def get_user_choice(won: bool) -> str:
    """Prompt the user to enter a game choice, 1, 2, or 3, which corresponds 
    to play, quit, and edit game settings, respectively. Return the valid 
    choice as a string. If won is True, give option to continue the game 
    instead of playing the game. """

    while True:
        if won:
            print("1. Continue Game.\n2. Exit Game.\n3. Game Settings.\n")
        else:
            print("Main Menu\n" + "-" * len("Main Menu"))
            print("1. Play Game. \n2. Quit.\n3. Game Settings.\n")

        program = input("Your choice: ")

        # Ensure that user enters a valid game choice.
        if program in VALID_GAME_CHOICES:
            return program
        else:
            print("{} is not a valid choice. Valid choices are"
                  .format(program)
                  + " ({}) for play, ({}) for quit, and ({}) for settings.\n"
                  .format(PLAY, QUIT, SETTINGS))


def get_valid_direction(key_bind_mode: dict) -> str:
    """Prompt the user to enter a direction w, a, s, or d, which correspond to 
    up, left, down, and right, respectively. Return the valid direction as a
    string."""

    while True:
        direction = input("\nEnter a direction to move: ")

        valid_direction = False 

        # Ensure the direction entered is valid.
        for key in key_bind_mode: 
            if key_bind_mode[key] == direction:
                valid_direction = True

        if valid_direction:
            return direction
        else:
            print("\nValid directions are {}, {}, {}, and {}. " 
                .format(key_bind_mode["up"], key_bind_mode["left"], 
                        key_bind_mode["down"], key_bind_mode["right"])
                + "Please try again.")


def generate_empty_board(game_tiles: list) -> list:
    """Generates a empty game board, which is a 4 by 4 two dimensional list
    with only 0s. 

    >>> generate_empty_board([]) 
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]] 
    """

    for i in range(BOARD_SIDE_LENGTH):
        game_tiles.append([0] * BOARD_SIDE_LENGTH)

    return game_tiles


def tile_shift(game_tiles: list, upwards: bool) -> list:
    """Shift the tiles in the grid game_tiles in the upwards or leftwards 
    direction. Return the new game tiles as a two dimensional list. 

    >>> tile_shift([[0, 0, 0, 0],
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 2]], 
                    "up") 
    [[0, 0, 0, 2], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0]]

    >>> tile_shift([[0, 0, 0, 0],
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [0, 0, 0, 2]], "left") 
    [[0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [0, 0, 0, 0], 
     [2, 0, 0, 0]]
    """

    shifted_tiles = generate_empty_board([])

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
    """Shift the tiles in the grid game_tiles in the leftwards direction. 
    Return the new game tiles as a two dimensional list. 

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

    reflected_tiles = generate_empty_board([])

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
    direction, based on the value of direction. Tiles can merge if they are 
    next to each other in the direction of the merge and are the same number. 
    Return the merged game tiles as a two dimensional list. 

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
                first_tile = game_tiles[row][col]
                second_tile = game_tiles[row + 1][col]

                # Two non-empty tiles of the same number in the same column
                # are on top of each other.
                if first_tile == second_tile and first_tile + second_tile != 0:
                    merge_score += first_tile + second_tile
                    merged_tiles[row][col] = first_tile + second_tile

                    merged_tiles[row + 1][col] = 0

    # Merge game board leftwards.
    else:
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH - 1):

                first_tile = game_tiles[row][col]
                second_tile = game_tiles[row][col + 1]

                # Two non-empty tiles of the same number in the same row
                # are beside each other.
                if first_tile == second_tile and first_tile + second_tile != 0:
                    merge_score += first_tile + second_tile
                    merged_tiles[row][col] = first_tile + second_tile

                    merged_tiles[row][col + 1] = 0

    return merged_tiles, merge_score


def add_random_tile(game_tiles: list) -> list:
    """Add a 2 or 4 tile to the grid, game_tiles, at a random empty tile."""

    # Random 2 or 4 tile.
    random_tile = TILE_BASE ** randint(1, 2)

    # Place new tile in random, empty tile spot. 
    while True:
        row = randint(0, 3)
        col = randint(0, 3)

        if game_tiles[row][col] == 0:
            game_tiles[row][col] = random_tile
            break

    return game_tiles


def check_tile(game_tiles: list, value: int) -> bool:
    """Return True if value is in the game board, game_tiles. 
    Otherwise, return False.

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
    leftwards consists of two tile shifts left, with on leftwards tile merge
    in between. Return the game board after the left move and the score
    accumulated from the move.

    >>> move_left([[0, 2, 2, 8], 
                   [4, 0, 0, 8], 
                   [0, 2, 0, 0], 
                   [2, 0, 0, 2]])
    [[4, 8, 0, 0], 
     [4, 8, 0, 0], 
     [2, 0, 0, 0], 
     [4, 0, 0, 0]]
    """

    game_tiles = tile_shift(game_tiles, False)
    game_tiles, score = merge_game_board(game_tiles, False)
    game_tiles = tile_shift(game_tiles, False)

    return game_tiles, score


def game_board_move(game_tiles: list, direction: str, 
                    key_bind_mode: dict) -> tuple:
    """Perform one move of the game board, in any direction (up, down, left, 
    or right). Return the game board after the move and the points earned from
    the move. 

    >>> game_board_move([[0, 0, 0, 2], 
                         [0, 2, 0, 0], 
                         [0, 4, 0, 0], 
                         [2, 0, 0, 0]], "w")
    ([[2, 2, 0, 2], 
      [0, 4, 0, 0], 
      [0, 0, 0, 0], 
      [0, 0, 0, 0]], 0)

    >>> game_board_move([[2, 2, 0, 2], 
                         [0, 4, 0, 0], 
                         [0, 0, 0, 0], 
                         [0, 0, 0, 0]], "a")
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

    # The game board did not change and no more random tiles can be added.
    # However, there are still possible moves.
    if moved_tiles == game_tiles:
        print("The move {}wards does not move any tiles.\n"
              .format(move_direction))

    return moved_tiles, score


def game_outcome(game_tiles: list, won: bool) -> str:
    """Return "win" if the user has won the round by creating the tile 
    2048 in game_tiles. Return "in progress" if any possible moves can be 
    made in game_tiles. Otherwise, return "loss"."""

    # If the user has not already created the 2048 tile, they have won.
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
    """Plays one single round of 2048. Return the score of the round."""

    # Every time two tiles are merged, the value of their sum is added to the
    # score.
    round_score = 0

    won = False

    game_tiles = []
    game_tiles = generate_empty_board(game_tiles)
    game_tiles[0][0] = 2048

    # Start with 2 tiles. 
    for i in range(STARTING_TILES):
        game_tiles = add_random_tile(game_tiles)

    for key in key_bind_mode: 
        print("{} : {}".format(key, key_bind_mode[key]))

    print()

    print_board(game_tiles)

    while game_outcome(game_tiles, won) != "loss":
        if check_tile(game_tiles, WINNING_TILE) and not won:
            print("\n😱 Hooray! You won! 😱")
            won = True
            program = get_user_choice(True)

            if program == QUIT:
                print("Exiting Game...\n")
                return
            else:
                print_board(game_tiles)

        direction = get_valid_direction(key_bind_mode)
        print()

        new_game_tiles, move_score = game_board_move(game_tiles, 
                                    direction, key_bind_mode)
        round_score += move_score

        # If the board does not have an empty square or the move performed did 
        # not change the game board, do not add a random tile. 
        if check_tile(new_game_tiles, EMPTY_TILE) and \
            new_game_tiles != game_tiles:

            new_game_tiles = add_random_tile(new_game_tiles)
            game_tiles = new_game_tiles 

        print_board(new_game_tiles)

    print() 
    if not won: 
        print("😢 Sorry, you lost the game. Better luck next time. 😢\n")

    print("🎉  Total Score: {} 🎉 \n".format(round_score))

    return round_score


def main():
    """The main game loop, with rules and a game overview."""

    print("Welcome to 2048.\n")

    print("Overview of the Game: \n")
    print("1. The objective of the game is to create the tile 2048 by merging"
          + " tiles together.")
    print("2. You can shift the tiles on the game board in 4 directions:"
          + " up, down, right, and left.")
    print("3. When two tiles of the same number are next to each other during"
          + " a merge, they will add together and merge into the same tile.")
    print("4. 2 and 4 tiles will be added to the board in random, empty tile"
          + " spots. If a tile cannot be added to the grid, you have lost.")
    print("5. You lose when there are no more empty tiles and no more"
          + " possible moves.\n")

    for i in range(GAME_BOARD_WIDTH): 
        print(".  ", end="")

    print("\n")

    high_score = 0

    program = PLAY
    key_bind_mode = MOVES_1

    while program != QUIT:
        program = get_user_choice(False)

        if program == PLAY:
            print("\nGame starting...\n")
            sleep(TIME_DELAY)
            round_score = game_round(key_bind_mode)

            if round_score > high_score: 
                high_score = round_score

        elif program == QUIT:
            if high_score != 0:
                print("\n🔥 Your highest score was {}. 🔥.".format(high_score))

            print("\n👋 Thanks for playing 2048. Goodbye! 👋")

        elif program == SETTINGS: 
            print("\nCurrent Keybinds: {}\n".format(key_bind_mode))
            key_bind_mode = choose_key_bind(key_bind_mode)
        else:
             print("Invalid menu choice. Please try again.")


if __name__ == "__main__":
    main()
