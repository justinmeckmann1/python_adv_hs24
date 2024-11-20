from game_logic_base import GameLogicBase
from player_sensehat import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState, check_win
from drop_state import DropState

class GameLogic(GameLogicBase):

    def __init__(self):
        super().__init__()
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        self._state = GameState.TURN_RED # alway start with player red

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
        return self._state