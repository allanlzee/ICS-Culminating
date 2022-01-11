GAME_BOARD_WIDTH = 23
TILE_LENGTH = 5
BOARD_SIDE_LENGTH = 4
EMPTY_BOARD = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]


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


# Game Logic 


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

    shifted_tiles = EMPTY_BOARD

    for col in range(BOARD_SIDE_LENGTH): 
        empty_position = 0 

        for row in range(BOARD_SIDE_LENGTH): 
            if direction == "up": 
                if game_tiles[row][col] != 0: 

                    shifted_tiles[empty_position][col] = game_tiles[row][col]
                    empty_position += 1 
            
            else: 
                if game_tiles[col][row] != 0:

                    shifted_tiles[col][empty_position] = game_tiles[col][row]
                    empty_position += 1

    return shifted_tiles


def reflect_grid(game_tiles: list, direction: str) -> list: 
    """Shift the tiles in the grid game_tiles in the leftwards direction. 
    Return the new game tiles as a two dimensional list. """

    reflected_tiles = EMPTY_BOARD
    
    for row in range(BOARD_SIDE_LENGTH): 
        
        for col in range(BOARD_SIDE_LENGTH): 
            if direction == "vertical":
                reflected_row = BOARD_SIDE_LENGTH - 1 - row

                reflected_tiles[row][col] = game_tiles[reflected_row][col]

            else: 
                reflected_column = BOARD_SIDE_LENGTH - 1 - col 
                reflected_tiles[row][col] = game_tiles[row][reflected_column]

    return reflected_tiles 
            

def game_round():
    """Plays one single round of 2048."""

    game_matrice = EMPTY_BOARD

    



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
