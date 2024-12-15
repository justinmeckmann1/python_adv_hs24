from game_logic import GameLogic
from game_state import GameState
from drop_state import DropState
from flask import Flask, request, jsonify
from flasgger import Swagger
import threading

"""
Connect Four Game Server Implementation

The server exposes the following API endpoints:
- GET /api/board: Returns the current state of the game board
- GET /api/state: Returns the current game state (whose turn, win state, etc.)
- POST /api/drop: Handles player moves by dropping tokens in specified columns

Key Components:
- Flask application for handling HTTP requests
- Swagger integration for API documentation
- Threading for handling automatic game resets
- GameLogic class integration for game state management

Usage:
    To start the server on a webserver:
    1. $HOME/miniconda/bin/conda init
    2. source ~/.bashrc
    3. conda activate myenv
    4. cd PYTHON_PROJECT/connect_four/
    5. nohup python3 game_logic_server.py > output.log 2>&1 &

Dependencies:
    - Flask
    - flasgger
    - threading
    - GameLogic, GameState, and DropState from local modules
"""

if __name__ == "__main__":
    game = GameLogic()
    app = Flask(__name__)
    swagger = Swagger(app)

    Reset_timer = threading.Timer(10.0, None)
    Reset_timer_lock = threading.Lock()  # Create a lock for Reset_timer

    def reset_board(): 
        """
        Resets the game board by creating a new GameLogic instance.
        This function is called automatically after a game ends.
        """
        global game
        print("Reset Game")
        game = GameLogic() #reset board
    
    @app.route('/api/board', methods=['GET'])
    def get_board():
        """
        Get the current state of the game board.
        ---
        tags:
           - Getting information about the current game 
        description: |
            The response is a dictionary with a single entry:
            - `board`: A 6x7 grid (as a list of lists) representing the game board.

            **Response Details**: 
            The response contains:
            - a dictionary which contains a single key-value pair whose key is `board`.
            - The value represents the current state of the game board. It is a
              list containing 6 lists, each of which contain 7 strings. Each
              string represents a game token:
                - `'X'`: Player token for red.
                - `'0'`: Player token for yellow.
                - `' '`: An empty cell.

            *Example*:
            ```json
            {
                "board": [
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ','0',' ',' '],
                    [' ',' ',' ','0','X',' ',' '],
                    [' ','X','0','X','X','0',' ']
                ]
            }
            ```
        responses:
            200:
                description: The current game board
                schema:
                    type: object
                    properties:
                        board:
                            type: array
                            description: The game board, represented as a list of 6 rows.
                            items:
                                type: array
                                description: A row of the game board, represented as 7 game tokens.
                                items:
                                    type: string
                                    description: A token in the game, represented by one of 'X', 'O', ' '
        """
        # print(f"GET /api/board received from {request.remote_addr}")
        # working implementation for GET /api/board
        # get the board from the local GameLogic object
        board = game.get_board()

        # return board to the caller via JSON response
        return jsonify( {"board": board} ), 200 # status code: 200 Ok

    @app.route('/api/state', methods=['GET'])
    def get_state():
        """
        Retrieve the current state of the game.
        ---
        tags:
           - Getting information about the current game 
        description: |
            The response is a dictionary with a single entry:
            - `state`: An integer number indicating the current state of the game. Possible values are:
                - `0` (TURN_RED):    It's Red's turn to play.
                - `1` (TURN_YELLOW): It's Yellow's turn to play.
                - `2` (WON_RED):     Red has won the game.
                - `3` (WON_YELLOW):  Yellow has won the game.
                - `4` (DRAW):        The game ends in a draw.

            *Example*:
            ```json
            { "state": 1 }
            ```
        responses:
            200:
                description: The current game state
                schema:
                    type: object
                    properties:
                        state:
                            type: integer
                            description: The current state of the game, represented as integer number [0..4]
                            example: 1
        """
        global Reset_timer #not really reentrent but it works
        state = game.get_state()
        #if GameState is a finished condition then start a timer to reset the game
        with Reset_timer_lock: # Due to multithreadting and if multiple requests happen exactly make a threading lock so it does not start 2 timers.
        # print(f"GET /api/state received from {request.remote_addr}")
            if (state in [GameState.WON_YELLOW, GameState.WON_RED, GameState.DRAW]) and (Reset_timer.is_alive()==False):
                # Start the timer
                # Set the timer to call reset_board after 10 seconds.
                Reset_timer = threading.Timer(10.0, reset_board)
                Reset_timer.start()
        return jsonify({"game_state": state.value}), 200  # status code: 200 Ok

    @app.route('/api/drop', methods=['POST'])
    def drop_token():
        """
        A player makes their move by dropping their token into the specified column.
        ---
        tags:
           - A player making their move
        description: |
            **Request Details**:
            The request body contains a dictionary containing the player's move details.

            *Example*:
            ```json
            { "column": 3, "player_id": "X" }
            ```
            **Response Details**: 
            The response is a dictionary with a single entry:
            - `drop_state`: An integer number indicating the state of drop. Possible values are:
                - `0` (DROP_OK):        Token dropped successfully
                - `1` (COLUMN_INVALID): The selected column is invalid
                - `2` (COLUMN_FULL):    The selected column is already full
                - `3` (WRONG_PLAYER):   A player made a move that is not theirs
            
            *Example*:
            ```json
            { "drop_state": 1 }
            ```
        parameters:
            - in: body
              name: body
              required: true
              description: The dictionary containing the player's move details.
              schema:
                type: object
                properties:
                    player_id:
                        type: string
                        description: The token of the player making the move, either 'X' or '0'.
                        example: 'X'
                    column:
                        type: integer
                        description: The column in which to drop the token (0-indexed).
                        example: 3
        responses:
            200:
                description: The current game state
                schema:
                    type: object
                    properties:
                        drop_state:
                            type: integer
                            description: A status code describing the result of the drop [0..3]
                            example: 1
            400:
                description: Fields 'player_id' and/or 'column' missing in request body.
                schema:
                    type: object
                    properties:
                        Error:
                            type: string
                            description: Textual desription of the error.
                            example: Fields 'player_id' and/or 'column' missing in request body.
        """
        # IMPLEMENT POST /api/drop HERE!
        request_dict = request.json
        print("------------------")
        print(request_dict)
        print("------------------")
        # print(f"GET /api/state received from {request.remote_addr}")
        if ("player_id" in request_dict and "column" in request_dict):
            DropState = game.drop_token(request_dict["player_id"],request_dict["column"])
            return jsonify({"drop_state": DropState.value}), 200 # status code: 200 Ok
        else:
            return jsonify(), 400 #Fields 'player_id' and/or 'column' missing in request body.

    


    # starting the server on all interfaces
    print("Game server start")
    app.run(host="0.0.0.0", debug=True)
    print("Game server exit")
