from sense_hat import SenseHat
from display_base import DisplayBase
from display_console import DisplayConsole
from display_sensehat import DisplaySensehat
from input_base import Keys
from input_console import InputConsole
from input_joystick import InputJoystick
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi


class PlayerSenseHat(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        # self._display = DisplayConsole()
        # self._input = InputConsole()
        sense = SenseHat()
        self._display = DisplaySensehat(sense)
        self._input = InputJoystick(sense)


if __name__ == "__main__":
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerSenseHat(GameToken.YELLOW)

    #Ansi.clear_screen()
    #Ansi.reset()
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    Ansi.reset()
    Ansi.gotoXY(1, 20)
    #print(board)
    print(f"Position: {pos}")
