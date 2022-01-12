from random import randint


# Graphics Constants
GAME_BOARD_WIDTH = 23
TILE_LENGTH = 5
BOARD_SIDE_LENGTH = 4

# Game Logic Constants
STARTING_TILES = 2
VALID_DIRECTIONS = ["w", "a", "s", "d"]
MOVES = {"w": "up",
         "s": "down",
         "a": "left",
         "d": "right"}
WINNING_TILE = 2048
EMPTY_TILE = 0
PLAY = "1"
QUIT = "2"


def print_board(matrix: str):
    """Print the game matrix."""

    for row in range(BOARD_SIDE_LENGTH):
        if row == 0:
            print("/" + "-" * GAME_BOARD_WIDTH + "\\")

        else:
            print("|" + "-" * GAME_BOARD_WIDTH + "|")

        print("|", end="")

        for column in range(4):
            print("{:>{width}}|".format(matrix[row][column],
                                        width=TILE_LENGTH), end="")

        print()

    print("\\" + "-" * GAME_BOARD_WIDTH + "/")


def get_user_choice(status: str) -> str:
    """Prompt the user to enter a game choice, 1 or 2, which corresponds to play
    and quit, respectively. Return the valid choice as a string."""

    while True:
        if status == "win":
            print("1. Continue Game.\n2. Exit Game.\n")
        else:
            print("Main Menu\n" + "-" * len("Main Menu"))
            print("1. Play Game. \n2. Quit.\n")

        program = input("Your choice: ")

        # Ensure that user enters a valid game choice.
        if program == PLAY or program == QUIT:
            return program
        else:
            print("{} is not a valid choice. Valid choices are".format(program)
                  + " ({}) for play and ({}) for quit.\n".format(PLAY, QUIT))


def get_valid_direction() -> str:
    """Prompt the user to enter a direction w, a, s, or d, which correspond to 
    up, left, down, and right, respectively. Return the valid direction as a
    string."""

    while True:
        direction = input("\nEnter a direction to move: ")

        # Ensure the direction entered is valid.
        if direction in VALID_DIRECTIONS:
            return direction
        else:
            print("\nValid directions are w, a, s, and d. Please try again.")


def generate_empty_board(game_tiles: list) -> list:

    for i in range(BOARD_SIDE_LENGTH):
        game_tiles.append([0] * BOARD_SIDE_LENGTH)

    return game_tiles


def tile_shift(game_tiles: list, direction: str) -> list:
    """Shift the tiles in the grid game_tiles in the upwards or leftwards direction. 
    Return the new game tiles as a two dimensional list. """

    shifted_tiles = []

    shifted_tiles = generate_empty_board(shifted_tiles)

    if direction == "up":
        for col in range(BOARD_SIDE_LENGTH):
            empty_position = 0

            for row in range(BOARD_SIDE_LENGTH):
                if game_tiles[row][col] != 0:
                    shifted_tiles[empty_position][col] = game_tiles[row][col]
                    empty_position += 1

    else:
        for col in range(BOARD_SIDE_LENGTH):
            empty_position = 0

            for row in range(BOARD_SIDE_LENGTH):
                if game_tiles[col][row] != 0:

                    shifted_tiles[col][empty_position] = game_tiles[col][row]
                    empty_position += 1

    return shifted_tiles


def reflect_grid(game_tiles: list, direction: str) -> list:
    """Shift the tiles in the grid game_tiles in the leftwards direction. 
    Return the new game tiles as a two dimensional list. """

    reflected_tiles = []

    reflected_tiles = generate_empty_board(reflected_tiles)

    if direction == "vertical":
        for row in range(BOARD_SIDE_LENGTH):
            reflected_tiles[row] = game_tiles[BOARD_SIDE_LENGTH - 1 - row]

    else:
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH):

                reflected_column = BOARD_SIDE_LENGTH - 1 - col
                reflected_tiles[row][col] = game_tiles[row][reflected_column]

    return reflected_tiles


def merge_game_board(game_tiles: list, direction: str) -> list:
    """Merge the tiles in the grid game_tiles in the upwards or leftwards 
    direction, based on the value of direction. Tiles can merge if they are 
    next to each other in the direction of the merge and are the same number. 
    Return the merged game tiles as a two dimensional list. """

    merge = False

    merged_tiles = game_tiles

    if direction == "up":
        for col in range(BOARD_SIDE_LENGTH):
            for row in range(BOARD_SIDE_LENGTH - 1):
                first_tile = game_tiles[row][col]
                second_tile = game_tiles[row + 1][col]

                if first_tile == second_tile and first_tile + second_tile != 0:
                    merged_tiles[row][col] = first_tile + second_tile
                    merged_tiles[row + 1][col] = 0

                    merge = True

    else:
        for row in range(BOARD_SIDE_LENGTH):
            for col in range(BOARD_SIDE_LENGTH - 1):

                first_tile = game_tiles[row][col]
                second_tile = game_tiles[row][col + 1]
                if first_tile == second_tile and first_tile + second_tile != 0:
                    merged_tiles[row][col] = first_tile + second_tile
                    merged_tiles[row][col + 1] = 0

                    merge = True

    if merge:
        return merged_tiles

    return game_tiles


def add_random_tile(game_tiles: list) -> list:
    """Add a random 2 or 4 tile to the grid, game_tiles."""

    random_tile = 2 ** randint(1, 2)

    while True:
        row = randint(0, 3)
        col = randint(0, 3)

        if game_tiles[row][col] == 0:
            game_tiles[row][col] = random_tile
            break

    return game_tiles


def check_tile(game_tiles: list, value: int) -> bool:
    """Return True if value is in the game board, game_tiles. 
    Otherwise, return False."""

    for row in game_tiles:
        if value in row:
            return True

    return False


def game_outcome(game_tiles: list) -> str:

    if check_tile(game_tiles, WINNING_TILE):
        return "win"

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

        return "loss"


def move_up(game_tiles: list) -> list:
    game_tiles = tile_shift(game_tiles, "up")
    game_tiles = merge_game_board(game_tiles, "up")
    game_tiles = tile_shift(game_tiles, "up")

    return game_tiles


def move_left(game_tiles: list) -> list:
    game_tiles = tile_shift(game_tiles, "left")
    game_tiles = merge_game_board(game_tiles, "left")
    game_tiles = tile_shift(game_tiles, "left")

    return game_tiles


def game_board_move(game_tiles: list, direction: str) -> list:

    moved_tiles = game_tiles
    direction = MOVES[direction]

    if direction == "up":
        moved_tiles = move_up(game_tiles)

    elif direction == "down":
        moved_tiles = reflect_grid(game_tiles, "vertical")
        moved_tiles = move_up(moved_tiles)
        moved_tiles = reflect_grid(moved_tiles, "vertical")

    elif direction == "left":
        moved_tiles = move_left(game_tiles)

    else:
        moved_tiles = reflect_grid(game_tiles, "horizontal")
        moved_tiles = move_left(moved_tiles)
        moved_tiles = reflect_grid(moved_tiles, "horizontal")

    # The game board did not change and no more random tiles can be added.
    if moved_tiles == game_tiles and not check_tile(moved_tiles, EMPTY_TILE):
        print("The move {}wards does not move any tiles.\n"
              .format(direction))

    return moved_tiles


def game_round():
    """Plays one single round of 2048."""
    won = False

    game_tiles = []
    game_tiles = generate_empty_board(game_tiles)

    for i in range(STARTING_TILES):
        game_tiles = add_random_tile(game_tiles)

    print_board(game_tiles)

    while game_outcome(game_tiles) != "loss":
        if check_tile(game_tiles, WINNING_TILE) and not won:
            print("Hooray! You won!")
            won = True
            program = get_user_choice("win")

            if program == QUIT:
                print("Exiting Game...\n")
                return
            else:
                print_board(game_tiles)

        direction = get_valid_direction()
        print()

        game_tiles = game_board_move(game_tiles, direction)

        if check_tile(game_tiles, EMPTY_TILE):
            game_tiles = add_random_tile(game_tiles)

        print_board(game_tiles)

    print("\nSorry, you lost the game. Better luck next time.\n")


def main():
    """The main game loop."""

    print("Welcome to 2048.\n")

    print("Overview of the Game: ")
    print("1. The objective of the game is to create the tile 2048.")
    print("2. You can shift the tiles on the game board in 4 directions: "
          + "up, down, right, and left.")
    print("3. When two tiles of the same number are next to each other, they " +
          "will add together and merge into the same tile, leaving a 0 tile.")
    print("4. Random 2, 4, and 8 tiles will be added to the board on 0 tiles.")
    print("5. You lose when there are no more 0 tiles and no more possible moves.\n")

    program = PLAY

    while program == PLAY:
        program = get_user_choice("start")

        if program == PLAY:
            print()
            game_round()
        else:
            print("\nThanks for playing 2048. Goodbye!")
            program = QUIT


if __name__ == "__main__":
    main()
