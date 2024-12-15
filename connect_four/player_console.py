from display_base import DisplayBase
from display_console import DisplayConsole
from input_base import Keys
from input_console import InputConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi


class PlayerConsole(PlayerBase):
    """
    Console-specific implementation of a player in Connect Four.
    
    Attributes:
        _display (DisplayConsole): Console-specific display handler
        _input (InputConsole): Console-specific input handler
        _player (GameToken): The player's token (inherited from PlayerBase)
    """
    
    def __init__(self, player: GameToken):  # Red or Yellow player
        """
        Initialize a console player with their game token.

        Args:
            player (GameToken): The token (RED or YELLOW) representing this player
        """
        super().__init__(player)
        self._display = DisplayConsole()
        self._input = InputConsole()

if __name__ == "__main__":
    # Create a board with one token
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerConsole(GameToken.YELLOW)

    #Ansi.clear_screen()
    #Ansi.reset()
    
    # Draw the board and let player make a move
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    
    # Reset cursor and display result
    Ansi.reset()
    Ansi.gotoXY(1, 20)
    #print(board)
    print(f"Position: {pos}")
