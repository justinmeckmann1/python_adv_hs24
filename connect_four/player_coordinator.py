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

# color = 'red'
color = 'yellow'

class PlayerCoordinator:
    def __init__(self):
        # initialize players
        if os.name != 'nt':
            self._player = PlayerSenseHat(GameToken.RED) if color == 'red' else PlayerSenseHat(GameToken.YELLOW)
        else:
            self._player = PlayerConsole(GameToken.RED) if color == 'red' else PlayerConsole(GameToken.YELLOW)

    def run(self, game: GameLogicBase):
        self._player.draw_board(game.get_board(), game.get_state())
        # play game until won or draw
        while (True):
            # Get current player based on state
            game_state = game.get_state()
            
            current_player = self._player if (
                (self._player.player_id == GameToken.RED and game_state == GameState.TURN_RED) or 
                (self._player.player_id == GameToken.YELLOW and game_state == GameState.TURN_YELLOW)
            ) else None
            
            current_token = (GameToken.RED if game_state == GameState.TURN_RED else GameToken.YELLOW)
            
            valid = DropState.COLUMN_INVALID
            
            self._player.draw_board(game.get_board(), game.get_state())
            
            while valid != DropState.DROP_OK and current_player is not None:
                column_to_drop = current_player.play_turn()
                valid = game.drop_token(current_token, column_to_drop)
            
            self._player.draw_board(game.get_board(), game.get_state())

            # Check if game is over 
            temp_gamestate = game.get_state()
            if temp_gamestate in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                winner_token = (GameToken.RED if temp_gamestate == GameState.WON_RED 
                            else GameToken.YELLOW)
                self._player.display_winner(winner_token)
                # current_player = (self._player_yellow if temp_gamestate == GameState.WON_RED #select the looser
                #             else self._player_red)
                # current_player.draw_board(game.get_board(), temp_gamestate) #draw board for the looser
                # current_player.display_winner(winner_token)
                break
            
            # If it's not our turn, wait a bit and update the board
            if self._player.player_id != game_state:
                self._player.draw_board(game.get_board(), game_state)
                game.wait_for_remote_move()

# start a remote game
if __name__ == '__main__':
    game = GameLogicClient(host='localhost:5000')
    game = GameLogicClient(host='localhost:5000')
    coordinator = PlayerCoordinator()
    coordinator.run(game)

