from game_logic_base import GameLogicBase
from game_state import GameState
from drop_state import DropState
from game_token import GameToken
import requests

class GameLogicClient(GameLogicBase):
    """
    Client implementation of the Connect Four game logic that communicates with a remote server.

    Attributes:
        _url (str): The base URL for the remote API endpoints
    """
    def __init__(self, host):
        """
        Initialize the GameLogicClient with a host address.

        Args:
            host (str): The host address of the remote server (with or without http/https protocol)
        """
        super().__init__()
        host = host.replace('http://', '').replace('https://', '')
        print(f"GameLogicClient initialized with host {host}")
        self._url = f'http://{host}/api'

    def get_board(self) -> list:
        """
        Retrieve the current game board state from the server.

        Returns:
            list: A 2D list representing the current game board
        """
        # call remote API
        response = requests.get(f"{self._url}/board")
        # return result to local caller
        return response.json().get("board")

    def get_state(self) -> GameState:
        """
        Retrieve the current game state from the server.

        Returns:
            GameState: The current state of the game (e.g., TURN_RED, TURN_YELLOW, etc.)
        """
        response = requests.get(f"{self._url}/state")
        return GameState(response.json().get("game_state"))
            
    def drop_token(self, player, column) -> DropState:
        """
        Attempt to drop a token in the specified column for the given player.

        Args:
            player (GameToken): The player making the move (RED or YELLOW)
            column (int): The column number where the token should be dropped (0-6)

        Returns:
            DropState: The result of the drop attempt (DROP_OK, COLUMN_FULL, etc.)
        """
        token = dict(player_id=player, column=column)
        response = requests.post(f"{self._url}/drop", json=token)
        return DropState(response.json().get("drop_state"))

if __name__ == '__main__':
    """
    Test programm to manually check if GameLogicClient is working.
    Limitations:
    - Implements both players at once--no distributed gameplay possible
    - Does not handle errors
    - Does not handle end of game gracefully
    """
    # local function
    def draw_board( board: list, state: GameState) -> None:
        """
        Draw the current game board and state to the console.

        Args:
            board (list): The current game board to display
            state (GameState): The current game state to display
        """
        print("0|1|2|3|4|5|6")
        for row in board:
            print('|'.join(row))
        print( f"GameState: {state}" )

    client = GameLogicClient("127.0.0.1")
    while( True ):
        game_state = client.get_state()
        board = client.get_board()

        draw_board( board, game_state )

        if game_state == GameState.TURN_RED or  game_state == GameState.TURN_YELLOW:
            player = GameToken.RED if game_state == GameState.TURN_RED else GameToken.YELLOW  
            column = int(input("Which colum to drop? "))    
            drop_state = client.drop_token( player, column )
            print( "drop_state:", drop_state )
        else: break # bail out if its neither RED's nor YELLOW's turn, i.e. WON or DRAW
    
    print("Game Over")
