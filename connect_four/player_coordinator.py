import os
if os.name != 'nt':
    from player_sensehat import PlayerSenseHat
from player_console import PlayerConsole
from game_token import GameToken
from game_state import *
from drop_state import DropState
from game_logic_base import GameLogicBase
from game_logic import GameLogic
from game_logic_client import GameLogicClient

class PlayerCoordinator:
    def __init__(self):
        # initialize local player
        if os.name == 'nt':
            self._local_player = PlayerConsole(GameToken.RED)
            # self._local_player = PlayerConsole(GameToken.YELLOW)

        else:
            self._local_player = PlayerSenseHat(GameToken.RED)
            # self._local_player = PlayerSenseHat(GameToken.YELLOW)


    def run(self, game: GameLogicClient):
        self._local_player.draw_board(game.get_board(), game.get_state())
        
        while True:
            game_state = game.get_state()
            
            # Only play when it's our turn
            if game_state == GameState.TURN_RED:
                valid = DropState.COLUMN_INVALID
                self._local_player.draw_board(game.get_board(), game_state)
                
                while valid != DropState.DROP_OK:
                    column_to_drop = self._local_player.play_turn()
                    valid = game.drop_token(GameToken.RED, column_to_drop)
                
                self._local_player.draw_board(game.get_board(), game.get_state())
            
            # Check if game is over
            if game_state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                self._local_player.draw_board(game.get_board(), game_state)
                break
            
            # If it's not our turn, wait a bit and update the board
            if game_state == GameState.TURN_YELLOW:
                self._local_player.draw_board(game.get_board(), game_state)
                game.wait_for_remote_move()

# start a remote game
if __name__ == '__main__':
    game = GameLogicClient()
    coordinator = PlayerCoordinator()
    coordinator.run(game)

