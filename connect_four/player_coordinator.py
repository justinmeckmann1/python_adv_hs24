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
import time

POLL_DELAY = 0.5 #Seconds

color = 'red'
# color = 'yellow'
host = 'virtualsquash.ch:5000'

class PlayerCoordinator:
    def __init__(self):
        # initialize players
        if os.name != 'nt':
            self._player = PlayerSenseHat(GameToken.RED) if color == 'red' else PlayerSenseHat(GameToken.YELLOW)
        else:
            self._player = PlayerConsole(GameToken.RED) if color == 'red' else PlayerConsole(GameToken.YELLOW)

    def run(self, game: GameLogicBase):
        self._player.draw_board(game.get_board(), game.get_state())
        opponentTurnState =  (GameState.TURN_YELLOW if self._player.player_id == GameToken.RED 
                            else GameState.TURN_RED)
        # play game until won or draw
        while (True):
            # Get current player based on state
            game_state = game.get_state()

            #Check if game is over
            if game_state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                winner_token = (GameToken.RED if game_state == GameState.WON_RED 
                            else GameToken.YELLOW)
                self._player.display_winner(winner_token)
                break

            #Wait aslong as its not your turn
            while(game_state == opponentTurnState):
                time.sleep(POLL_DELAY)
                game_state = game.get_state()

            self._player.draw_board(game.get_board(), game_state)
            #Check again if game is over
            if game_state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                winner_token = (GameToken.RED if game_state == GameState.WON_RED 
                            else GameToken.YELLOW)
                self._player.display_winner(winner_token)
                break

            # Player's turn
            valid = DropState.COLUMN_INVALID
            while valid != DropState.DROP_OK:
                column_to_drop = self._player.play_turn()
                valid = game.drop_token(self._player.player_id, column_to_drop)
            self._player.draw_board(game.get_board(), game.get_state())

# start a remote game
if __name__ == '__main__':
    game = GameLogicClient(host=host)
    coordinator = PlayerCoordinator()
    while(True):
        coordinator.run(game)
        time.sleep(1) #wait for restart

