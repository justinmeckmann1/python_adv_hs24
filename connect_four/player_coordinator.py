from player_sensehate import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import *
from drop_state import DropState

class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = PlayerSenseHat(GameToken.RED)  # X
        self._player_yellow = PlayerSenseHat(GameToken.YELLOW)  # 0
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        self._state = GameState.TURN_RED

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

    def run(self):
        # play game until won or draw
        while (True):
            # Get current player based on state
            current_player = (self._player_red if self._state == GameState.TURN_RED 
                            else self._player_yellow)
            current_token = (GameToken.RED if self._state == GameState.TURN_RED 
                           else GameToken.YELLOW)
            
            # Player's turn
            valid = DropState.COLUMN_INVALID
            current_player.draw_board(self._board, self._state)
            while valid != DropState.DROP_OK:
                column_to_drop = current_player.play_turn()
                valid = self.drop_token(current_token, column_to_drop)
            
            # Check if game is over 
            if check_win(self._board) in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                current_player.draw_board(self._board, self._state)
                # do something to display winner 
                break
            
            # Switch turns
            self._state = (GameState.TURN_YELLOW if self._state == GameState.TURN_RED 
                          else GameState.TURN_RED)


# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
