from game_logic_base import GameLogicBase
from game_token import GameToken
from game_state import GameState, check_win
from drop_state import DropState
import random

"""
Game Logic Implementation for Connect Four

Classes:
    GameLogic: Main game logic implementation handling board state and moves
"""

class GameLogic(GameLogicBase):
    """
    Implementation of Connect Four game logic.

    Attributes:
        _board (List[List[GameToken]]): 6x7 game board grid
        __starter_state (GameState): Randomly chosen initial player's turn
    """
    def __init__(self):
        """
        Initialize a new game board and randomly select starting player.

        The board is created as a 6x7 grid of empty tokens, and the starting
        player (RED or YELLOW) is chosen randomly.
        """
        super().__init__()
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        if random.getrandbits(1):
            self.__starter_state = GameState.TURN_RED
        else:
            self.__starter_state = GameState.TURN_YELLOW

    def drop_token(self, player: GameToken, column: int) -> DropState:
        """
        Attempt to drop a player's token in the specified column.

        Args:
            player (GameToken): The player's token (RED or YELLOW)
            column (int): The column index where the token should be dropped (0-6)

        Returns:
            DropState: Status of the drop attempt:
                - DROP_OK: Token was successfully placed
                - COLUMN_INVALID: Column index is out of bounds
                - COLUMN_FULL: Selected column has no empty spaces
        """
        # check if the column is valid (0..6) => return the appropriate DropState
        if(column<=-1 or column>=len(self._board[0])):
            return DropState.COLUMN_INVALID
        
        # check if the column is full => return the appropriate DropState
        if(self._board[0][column] != GameToken.EMPTY):
            return DropState.COLUMN_INVALID

        # insert token into board (column = column_to_drop)
        for row in range(len(self._board)-1,-1,-1):
            if(self._board[row][column] == GameToken.EMPTY):
                self._board[row][column] = player
                break
    
        return DropState.DROP_OK

    def get_state(self) -> GameState:
        """
        Determine the current state of the game.

        Returns:
            GameState: Current game state:
                - WON_RED: Red player has won
                - WON_YELLOW: Yellow player has won
                - DRAW: Game is a draw
                - TURN_RED: Red player's turn
                - TURN_YELLOW: Yellow player's turn
        """
        
        game_result = check_win(self._board)
        
        # check if game is over and if so, return the results
        if game_result in [GameState.WON_RED, GameState.WON_YELLOW, GameState.DRAW]:
            
            return game_result

        # else, return the current state
        temp_RedCount = 0
        temp_YellowCount = 0
        # Iterate over the board to count RED tokens
        for row in self._board:
            for col in row:
                if col == GameToken.RED:
                    temp_RedCount += 1
                if col == GameToken.YELLOW:
                    temp_YellowCount += 1
        if temp_YellowCount == temp_RedCount:
            return self.__starter_state
        else:
            if self.__starter_state == GameState.TURN_RED:
                return GameState.TURN_YELLOW
            else:
                return GameState.TURN_RED
    
