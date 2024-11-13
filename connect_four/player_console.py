from display_base import DisplayBase
from display_console import DisplayConsole
from input_base import Keys
from input_console import InputConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi


class PlayerConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        self._display = DisplayConsole()
        self._input = InputConsole()


    # def play_turn(self) -> int:
    #     # return desired column from user input (0..6)
    #     temp_position = 0
    #     self._display.draw_token(temp_position,-1,self.player_id)
    #     while True:
    #         key = self._input.read_key()
    #         if key == Keys.ENTER:
    #             self._display.draw_token(temp_position,-1,GameToken.EMPTY)
    #             break
    #         if (key == Keys.LEFT): 
    #             if(temp_position >= 1):
    #                 self._display.draw_token(temp_position,-1,GameToken.EMPTY)
    #                 temp_position -= 1
    #                 self._display.draw_token(temp_position,-1,self.player_id)
    #         if (key == Keys.RIGHT):  
    #             if(temp_position <= self._display.get_x_grid()-2):
    #                 self._display.draw_token(temp_position,-1,GameToken.EMPTY)
    #                 temp_position += 1
    #                 self._display.draw_token(temp_position,-1,self.player_id)
    #     return temp_position

    # def draw_board(self, board: list, state: GameState):
    #     # draw grid with tokens 
    #     self._display.draw_grid(len(board[0]),len(board))
    #     for y_index, row in enumerate(board):
    #         for x_index, token in enumerate(row):
    #             self._display.draw_token(x_index,y_index,token)

if __name__ == "__main__":
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerConsole(GameToken.YELLOW)

    #Ansi.clear_screen()
    #Ansi.reset()
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    Ansi.reset()
    Ansi.gotoXY(1, 20)
    #print(board)
    print(f"Position: {pos}")
