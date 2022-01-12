from random import randint 


# Graphics Constants 
GAME_BOARD_WIDTH = 23
TILE_LENGTH = 5
BOARD_SIDE_LENGTH = 4

# Game Logic Constants 
STARTING_TILES = 2 
VALID_DIRECTIONS = ["w", "a", "s", "d"]
WINNING_TILE = 2048 
EMPTY_TILE = 0 


def get_valid_direction() -> str: 

    while True: 
        direction = input("Enter a direction to move: ")

        if direction in VALID_DIRECTIONS: 
            return direction 
        else: 
            print("\nValid directions are w, a, s, and d. Please try again.\n")


def generate_empty_board(game_tiles: list) -> list: 

    for i in range(BOARD_SIDE_LENGTH):
        game_tiles.append([0] * 4)

    return game_tiles 


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



def game_end(game_matrice: list) -> str:
    """Return "win" if the number 2048 appears in game_matrice.
    Return "lose" if there are no more 0s in game_matrice and there
    are no more possible moves. Otherwise, return "progress"."""

    zeros = False

    # Check for win
    for row in range(4):
        if 0 in row:
            zeros = True

        for column in range(4):
            if game_matrice[row][column] == 2048:
                return "win"

    # Check if moves are possible
    if zeros:
        return "progress"

    
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
            

def merge_grid(game_tiles: list, direction: str) -> list: 
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


def check_for_tile(game_tiles: list, value: int) -> bool: 
    """Return True if value is in the game grid, game_tiles. 
    Otherwise, return False."""

    for row in game_tiles: 
        if value in row: 
            return True 
    
    return False 


def game_status(game_tiles: list) -> str: 

    if check_for_tile(game_tiles, WINNING_TILE): 
        return "win" 

    elif check_for_tile(game_tiles, EMPTY_TILE): 
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
                if game_tiles[row][col] == game_tiles[row][col + 1]:
                    return "in progress"

        return "loss"


def move_up(game_tiles: list) -> str: 
    game_tiles = tile_shift(game_tiles, "up") 
    game_tiles = merge_grid(game_tiles, "up") 
    game_tiles = tile_shift(game_tiles, "up")

    return game_tiles 


def move_left(game_tiles: list) -> str: 
    game_tiles = tile_shift(game_tiles, "left") 
    game_tiles = merge_grid(game_tiles, "left")
    game_tiles = tile_shift(game_tiles, "left") 

    return game_tiles 


def grid_move(game_tiles: list, direction: str) -> list:
    if direction == "w": 
        return move_up(game_tiles)

    elif direction == "s":
        game_tiles = reflect_grid(game_tiles, "vertical") 
        game_tiles = move_up(game_tiles)
        game_tiles = reflect_grid(game_tiles, "vertical") 

    elif direction == "a": 
        return move_left(game_tiles)

    else: 
        game_tiles = reflect_grid(game_tiles, "horizontal")
        game_tiles = move_left(game_tiles)
        game_tiles = reflect_grid(game_tiles, "horizontal")

    return game_tiles 


def game_round():
    """Plays one single round of 2048."""

    game_tiles = []
    game_tiles = generate_empty_board(game_tiles)
    
    for i in range(STARTING_TILES):
        game_tiles = add_random_tile(game_tiles)

    print_board(game_tiles)
    print()

    while game_status(game_tiles) != "loss": 
        direction = get_valid_direction() 
        print() 

        game_tiles = grid_move(game_tiles, direction) 
        game_tiles = add_random_tile(game_tiles)
        print_board(game_tiles)


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

    game_round()


if __name__ == "__main__":
    main()
