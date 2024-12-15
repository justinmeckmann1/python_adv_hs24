from display_base import *
from game_state import *
from input_base import InputBase
from input_base import Keys



class PlayerBase:
    """
    Base class for representing a player in the game.

    This class provides an interface for player actions, including
    making a move and drawing the game board. Subclasses must implement
    the required methods to provide specific player behavior.
    """

    def __init__(self, player: GameToken):
        """
        Initialize the player with a specific game token.

        Args:
        - player: The token representing the player (e.g., RED or YELLOW).
        """
        self._player = player
        self._input = InputBase()
        self._display = DisplayBase()
    def play_turn(self) -> int:
        """
        Asks the player to play their turn.

        Returns:
            int: The column index where the player drops their token.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        temp_position = 0
        self._display.draw_token(temp_position,-1,self.player_id)
        while True:
            key = self._input.read_key()
            if key == Keys.ENTER:
                self._display.draw_token(temp_position,-1,GameToken.EMPTY)
                break
            if (key == Keys.LEFT): 
                if(temp_position >= 1):
                    self._display.draw_token(temp_position,-1,GameToken.EMPTY)
                    temp_position -= 1
                    self._display.draw_token(temp_position,-1,self.player_id)
            if (key == Keys.RIGHT):  
                if(temp_position <= self._display.get_x_grid()-2):
                    self._display.draw_token(temp_position,-1,GameToken.EMPTY)
                    temp_position += 1
                    self._display.draw_token(temp_position,-1,self.player_id)
        return temp_position

    def draw_board(self, board: list, state: GameState) -> None:
        """
        Draw the game board for the player.

        Parameters:
        - board: The current state of the game board.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        self._display.draw_grid(len(board[0]),len(board))
        for y_index, row in enumerate(board):
            for x_index, token in enumerate(row):
                self._display.draw_token(x_index,y_index,token)

    @property
    def player_id(self) -> GameToken:
        """
        Get the player's token.

        Returns:
            GameToken: The token representing the player.
        """
        return self._player
    
    def display_winner(self, token: GameToken) -> None:
        """
        Draw something to indicate the winner

        Args:
        - token: The token of the winner
        """
        self._display.draw_winner(token)
