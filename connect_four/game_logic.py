from game_logic_base import GameLogicBase
from game_token import GameToken
from game_state import GameState, check_win
from drop_state import DropState
import random

class GameLogic(GameLogicBase):

    def __init__(self):
        super().__init__()
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        if random.getrandbits(1):
            self.__starter_state = GameState.TURN_RED
        else:
            self.__starter_state = GameState.TURN_YELLOW

    def drop_token(self, player: GameToken, column: int) -> DropState:
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
    
