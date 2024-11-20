import os
if os.name != 'nt':
    from player_sensehat import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import *
from drop_state import DropState
from game_logic_base import GameLogicBase
from game_logic import GameLogic

class PlayerCoordinator:
    def __init__(self):
        # initialize players
        if os.name == 'nt':
            self._player_red = PlayerConsole(GameToken.RED)  # X
            self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        else:
            self._player_red = PlayerConsole(GameToken.RED)  # X
            self._player_yellow = PlayerSenseHat(GameToken.YELLOW)  # 0

    def run(self, game: GameLogicBase):
        self._player_red.draw_board(game.get_board(), game.get_state())
        self._player_yellow.draw_board(game.get_board(), game.get_state())
        # play game until won or draw
        while (True):
            # Get current player based on state
            current_player = (self._player_red if game.get_state() == GameState.TURN_RED 
                            else self._player_yellow)
            current_token = (GameToken.RED if current_player == self._player_red 
                           else GameToken.YELLOW)
            
            # Player's turn
            valid = DropState.COLUMN_INVALID
            current_player.draw_board(game.get_board(), game.get_state())
            while valid != DropState.DROP_OK:
                column_to_drop = current_player.play_turn()
                valid = game.drop_token(current_token, column_to_drop)
            current_player.draw_board(game.get_board(), game.get_state())

            # Check if game is over 
            if check_win(game.get_board()) in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                current_player = (self._player_yellow if game.get_state() == GameState.TURN_RED #select the looser
                            else self._player_red)
                current_player.draw_board(game.get_board(), game.get_state()) #draw board for the looser
                # do something to display winner 
                break
            
            # Switch turns
            state = (GameState.TURN_YELLOW if game.get_state() == GameState.TURN_RED 
                          else GameState.TURN_RED)
            game.set_state(state)

# start a local game
if __name__ == '__main__':
    game = GameLogic()
    coordinator = PlayerCoordinator()
    coordinator.run(game)

