import os
if os.name != 'nt':
    from player_sensehat import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import *
from drop_state import DropState
from game_logic_base import GameLogicBase
from game_logic import GameLogic
from game_logic_client import GameLogicClient
import time
import random

POLL_DELAY = 0.5 #Seconds

color = 'red'
#color = 'yellow'
host = 'eee-w014-104.simple.eee.intern:5000'


def best_drop_position(board, player_token):
    """
    Determines the best column to drop a token for the current player using a Minimax algorithm.

    Args:
        board (list[list[GameToken]]): The game board as a 2D list.
        player_token (GameToken): The token of the current player (RED or YELLOW).

    Returns:
        int: The index of the best column to drop the token.
    """
    ROWS = len(board)
    COLS = len(board[0])
    MAX_DEPTH = 4

    def is_valid_move(col):
        return board[0][col] == GameToken.EMPTY

    def simulate_drop(col, token):
        """Simulate dropping a token in the specified column."""
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == GameToken.EMPTY:
                board[row][col] = token
                return row

    def undo_drop(row, col):
        """Undo a simulated drop."""
        board[row][col] = GameToken.EMPTY

    def check_winning_move(row, col, token):
        """Check if placing a token creates a winning move."""
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal (bottom-left to top-right)
            [(1, -1), (-1, 1)],  # Diagonal (top-left to bottom-right)
        ]

        for direction in directions:
            count = 1
            for dx, dy in direction:
                r, c = row, col
                while 0 <= r + dx < ROWS and 0 <= c + dy < COLS and board[r + dx][c + dy] == token:
                    count += 1
                    r += dx
                    c += dy
                if count >= 4:
                    return True
        return False

    def evaluate_board(token):
        """Evaluate the board state and return a score for the current player."""
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == token:
                    score += evaluate_position(row, col, token)
                elif board[row][col] != GameToken.EMPTY:
                    opponent_token = GameToken.RED if token == GameToken.YELLOW else GameToken.YELLOW
                    score -= evaluate_position(row, col, opponent_token)
        return score

    def evaluate_position(row, col, token):
        """Evaluate the strength of a given position."""
        score = 0
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal (bottom-left to top-right)
            [(1, -1), (-1, 1)],  # Diagonal (top-left to bottom-right)
        ]

        for direction in directions:
            count = 1
            open_ends = 0
            for dx, dy in direction:
                r, c = row, col
                while 0 <= r + dx < ROWS and 0 <= c + dy < COLS and (board[r + dx][c + dy] == token or board[r + dx][c + dy] == GameToken.EMPTY):
                    if board[r + dx][c + dy] == token:
                        count += 1
                    elif board[r + dx][c + dy] == GameToken.EMPTY:
                        open_ends += 1
                    r += dx
                    c += dy
                if count >= 4:
                    return float('inf')  # Immediate win
            if open_ends > 0:
                score += count * (open_ends + 1)
        return score

    def minimax(depth, maximizing_player, alpha, beta):
        """Minimax algorithm with alpha-beta pruning."""
        opponent_token = GameToken.RED if player_token == GameToken.YELLOW else GameToken.YELLOW

        # Base cases
        if depth == 0:
            return evaluate_board(player_token), None

        valid_moves = [col for col in range(COLS) if is_valid_move(col)]
        if not valid_moves:
            return evaluate_board(player_token), None

        if maximizing_player:
            max_eval = -float('inf')
            best_col = None
            for col in valid_moves:
                row = simulate_drop(col, player_token)
                if check_winning_move(row, col, player_token):
                    undo_drop(row, col)
                    return float('inf'), col
                eval, _ = minimax(depth - 1, False, alpha, beta)
                undo_drop(row, col)
                if eval > max_eval:
                    max_eval = eval
                    best_col = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_col
        else:
            min_eval = float('inf')
            best_col = None
            for col in valid_moves:
                row = simulate_drop(col, opponent_token)
                if check_winning_move(row, col, opponent_token):
                    undo_drop(row, col)
                    return -float('inf'), col
                eval, _ = minimax(depth - 1, True, alpha, beta)
                undo_drop(row, col)
                if eval < min_eval:
                    min_eval = eval
                    best_col = col
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_col

    # Start the minimax algorithm
    _, best_column = minimax(MAX_DEPTH, True, -float('inf'), float('inf'))
    return best_column if best_column is not None else -1



class PlayerCoordinator:
    """
    Coordinates players actions and game flow in a networked Connect Four game.
    
    Attributes:
        _player (PlayerConsole | PlayerSenseHat): The local player instance

    """
    def __init__(self):
        """
        Initialize the player coordinator with appropriate player type.
        """
        # initialize players
        if os.name != 'nt':
            self._player = PlayerSenseHat(GameToken.RED) if color == 'red' else PlayerSenseHat(GameToken.YELLOW)
        else:
            self._player = PlayerConsole(GameToken.RED) if color == 'red' else PlayerConsole(GameToken.YELLOW)

    def run(self, game: GameLogicBase):
        """
        Run the networked game loop, coordinating with remote player.
        
        Args:
            game (GameLogicBase): The game logic instance managing rules and state.
        
        """
        self._player.draw_board(game.get_board(), game.get_state())
        opponentTurnState =  (GameState.TURN_YELLOW if self._player.player_id == GameToken.RED 
                            else GameState.TURN_RED)
        # play game until won or draw
        while (True):
            # Get current player based on state
            game_state = game.get_state()

            #Check if game is over
            if game_state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                if game_state in [GameState.WON_YELLOW, GameState.WON_RED]:
                    winner_token = (GameToken.RED if game_state == GameState.WON_RED 
                                    else GameToken.YELLOW)
                    self._player.display_winner(winner_token)
                break

            #Wait aslong as its not your turn
            while(game_state == opponentTurnState):
                time.sleep(POLL_DELAY)
                game_state = game.get_state()

            self._player.draw_board(game.get_board(), game_state)
            #Check again if game is over
            if game_state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                if game_state in [GameState.WON_YELLOW, GameState.WON_RED]:
                    winner_token = (GameToken.RED if game_state == GameState.WON_RED 
                                    else GameToken.YELLOW)
                    self._player.display_winner(winner_token)
                break

            # Player's turn
            valid = DropState.COLUMN_INVALID
            while valid != DropState.DROP_OK:
                column_to_drop = best_drop_position(game.get_board(),self._player.player_id)
                try:
                    valid = game.drop_token(self._player.player_id, column_to_drop)
                except:
                    while valid != DropState.DROP_OK:
                        valid = game.drop_token(self._player.player_id, random.randint(0,6))
                        print("random!!!!!")

# start a remote game
if __name__ == '__main__':
    game = GameLogicClient(host=host)
    coordinator = PlayerCoordinator()
    while(True):
        coordinator.run(game)
        time.sleep(1) #wait for restart

