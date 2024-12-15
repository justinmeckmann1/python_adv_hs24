from enum import Enum
from game_token import GameToken


class GameState(Enum):
    """
    Enum class representing different states of the game.
    
    Attributes:
        TURN_RED (int): Indicates it's Red player's turn (value: 0)
        TURN_YELLOW (int): Indicates it's Yellow player's turn (value: 1)
        WON_RED (int): Indicates Red player has won (value: 2)
        WON_YELLOW (int): Indicates Yellow player has won (value: 3)
        DRAW (int): Indicates the game ended in a draw (value: 4)
    """
    TURN_RED = 0          # It's Red's turn to play
    TURN_YELLOW = 1       # It's Yellow's turn to play
    WON_RED = 2           # Red has won the game
    WON_YELLOW = 3        # Yellow has won the game
    DRAW = 4              # The game ends in a draw


def check_win(board: list) -> GameState:
    """
    Checks the current state of the Connect Four game board.

    Args:
        board: A 2D list representing the game board where each cell contains a GameToken
              (RED, YELLOW, or EMPTY)

    Returns:
        GameState: The current state of the game. Possible returns are:
            - GameState.WON_RED: If red player has won
            - GameState.WON_YELLOW: If yellow player has won
            - GameState.DRAW: If the game is a draw (board is full)
            - GameState.TURN_RED: If the game is still ongoing (default state)
    """
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if (row[i] != GameToken.EMPTY and 
                row[i] == row[i + 1] == row[i + 2] == row[i + 3]):
                return GameState.WON_RED if row[i] == GameToken.RED else GameState.WON_YELLOW

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if (board[row][col] != GameToken.EMPTY and
                board[row][col] == board[row + 1][col] == 
                board[row + 2][col] == board[row + 3][col]):
                return GameState.WON_RED if board[row][col] == GameToken.RED else GameState.WON_YELLOW

    # Check diagonal (positive slope)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if (board[row][col] != GameToken.EMPTY and
                board[row][col] == board[row + 1][col + 1] ==
                board[row + 2][col + 2] == board[row + 3][col + 3]):
                return GameState.WON_RED if board[row][col] == GameToken.RED else GameState.WON_YELLOW

    # Check diagonal (negative slope)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if (board[row][col] != GameToken.EMPTY and
                board[row][col] == board[row - 1][col + 1] ==
                board[row - 2][col + 2] == board[row - 3][col + 3]):
                return GameState.WON_RED if board[row][col] == GameToken.RED else GameState.WON_YELLOW

    # Check for draw (full board)
    if all(token != GameToken.EMPTY for row in board for token in row):
        return GameState.DRAW

    # Game is still ongoing
    return GameState.TURN_RED #default open as red

if __name__ == '__main__':
    s = GameState.TURN_RED
    print(f"GameState {s}, Type: {type(s)}, Value: {s.value}")
