
from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState


class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = PlayerConsole(GameToken.RED)  # X
        self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        self._state = GameState.TURN_RED

    def drop_token(self, player: GameToken, column: int) -> DropState:
        # TODO check if the column is valid (0..6) => return the appropriate DropState
        # TODO check if the column is full => return the appropriate DropState
        # TODO insert token into board (column = column_to_drop)
        if(column<=-1 or column>=len(self._board[0])):
            return DropState.COLUMN_INVALID
        
        if(self._board[0][column] != GameToken.EMPTY):
            return DropState.COLUMN_INVALID

        for row in range(len(self._board)-1,-1,-1):
            if(self._board[row][column] == GameToken.EMPTY):
                self._board[row][column] = player
                break
    
        return DropState.DROP_OK

    def run(self):
        # play game until won or draw
        while (True):
            valid = DropState.COLUMN_INVALID
            self._player_red.draw_board(self._board, self._state)
            column_to_drop = self._player_red.play_turn()  # get the move of the player
            while(valid != DropState.DROP_OK):
                valid = self.drop_token(GameToken.RED, column_to_drop)
            valid = DropState.COLUMN_INVALID

            self._player_yellow.draw_board(self._board, self._state)
            column_to_drop = self._player_yellow.play_turn()  # get the move of the player
            while(valid != DropState.DROP_OK):
                valid = self.drop_token(GameToken.YELLOW, column_to_drop)
            valid = DropState.COLUMN_INVALID


# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
