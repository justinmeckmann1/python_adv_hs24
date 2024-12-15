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
    """    
    Coordinates player actions and game flow in a networked Connect Four game.
    Attributes:
        _player_red (PlayerConsole | PlayerSenseHat): The red player instance
        _player_yellow (PlayerConsole | PlayerSenseHat): The yellow player instance
    """

    def __init__(self):
        """
        Initialize the player coordinator with appropriate player types.
        """
        
        # initialize players
        if os.name == 'nt': # Windows (use Console)
            self._player_red = PlayerConsole(GameToken.RED)  # X
            self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        else: # Raspberry Pi (use SenseHat)
            self._player_red = PlayerSenseHat(GameToken.RED)  # X
            self._player_yellow = PlayerSenseHat(GameToken.YELLOW)  # 0

    def run(self, game: GameLogicBase):
        """
        Run the local game loop, coordinating turns between two players.

        Args:
            game (GameLogicBase): The game logic instance managing rules and state
        """
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
            temp_gamestate = game.get_state()
            if temp_gamestate in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]:
                winner_token = (GameToken.RED if temp_gamestate == GameState.WON_RED 
                            else GameToken.YELLOW)
                current_player.display_winner(winner_token)
                current_player = (self._player_yellow if temp_gamestate == GameState.WON_RED #select the looser
                            else self._player_red)
                current_player.draw_board(game.get_board(), temp_gamestate) #draw board for the looser
                current_player.display_winner(winner_token)
                break

# start a local game
if __name__ == '__main__':
    game = GameLogic()
    coordinator = PlayerCoordinator()
    coordinator.run(game)

