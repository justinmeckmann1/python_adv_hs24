import os
if os.name != 'nt':
    from player_sensehat import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import *
from drop_state import DropState
from game_logic import GameLogic

class PlayerCoordinator:
    def __init__(self):
        # initialize players
        if os.name == 'nt':
            self._player_red = PlayerConsole(GameToken.RED)  # X
            self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        else:
            self._player_red = PlayerSenseHat(GameToken.RED)  # X
            self._player_yellow = PlayerSenseHat(GameToken.YELLOW)  # 0
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        self._state = GameState.TURN_RED

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
            current_player.draw_board(game._board, game._state)
            while valid != DropState.DROP_OK:
                column_to_drop = current_player.play_turn()
                valid = game.drop_token(current_token, column_to_drop)
            current_player.draw_board(game._board, game._state)

            # Check if game is over 
            if check_win(game._board) in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                #current_player.draw_board(self._board, self._state)
                # do something to display winner 
                break
            
            # Switch turns
            self._state = (GameState.TURN_YELLOW if self._state == GameState.TURN_RED 
                          else GameState.TURN_RED)

# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    game = GameLogic()
    coordinator.run()
