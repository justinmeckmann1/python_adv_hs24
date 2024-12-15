from sense_hat import SenseHat
from game_token import GameToken
from display_base import DisplayBase


class DisplaySensehat(DisplayBase):
    """
Display implementation for the Raspberry Pi Sensehat.

Args:
    p_sense (SenseHat): An initialized Sense HAT object for LED matrix control

Attributes:
    __CLEAR (tuple): RGB color for empty spaces (0,0,0)
    __GRAY (tuple): RGB color for grid background (50,50,50)
    __RED (tuple): RGB color for player 1 tokens (255,0,0)
    __YELLOW (tuple): RGB color for player 2 tokens (255,255,0)
    __X_MAX_LENGTH (int): Maximum horizontal grid size (8)
    __Y_MAX_LENGTH (int): Maximum vertical grid size (8)

Raises:
    ValueError: If grid dimensions are too small (< 3x3)
    ValueError: If grid dimensions exceed LED matrix size
    ValueError: If invalid token type is provided
    ValueError: If token placement is out of grid bounds
"""
    __CLEAR = (0,0,0)
    __GRAY = (50,50,50)
    __RED = (255,0,0)
    __YELLOW = (255,255,0)
    __X_MAX_LENGHT = 8
    __Y_MAX_LENGHT = 8
    def __init__(self, p_sense:SenseHat):
        """
        Initializes a new Sense HAT display instance.

        Args:
            p_sense (SenseHat): An initialized Sense HAT object for controlling the LED matrix
        """
        super().__init__()
        self.__grid_x = 0
        self.__grid_y = 0
        self.sense = p_sense

    def __draw_selector(self, x:int, p_color) -> None:
        """
        Draws a selector indicator at the specified column with the given color.

        Args:
            x (int): The horizontal position (column) for the selector (0-based)
            p_color (tuple): RGB color tuple for the selector
        """
        self.sense.set_pixel(x,(self.__Y_MAX_LENGHT-self.__grid_y)-1,p_color)

    def __clear_selector(self, x:int) -> None:
        """
        Clears the selector indicator at the specified column.

        Args:
            x (int): The horizontal position (column) to clear (0-based)
        """
        self.sense.set_pixel(x,(self.__Y_MAX_LENGHT-self.__grid_y)-1,self.__CLEAR)

    def get_x_grid(self):
        """
        Returns the current grid width.

        Returns:
            int: The number of columns in the grid
        """
        return self.__grid_x
    
    def draw_grid(self, x:int, y:int) -> None:
        """
        Initializes and draws the game grid on the LED matrix.

        Args:
            x (int): Width of the grid (number of columns)
            y (int): Height of the grid (number of rows)

        Raises:
            ValueError: If grid dimensions are too small (< 3x3)
            ValueError: If grid dimensions exceed LED matrix size
        """
        self.__grid_x = x
        self.__grid_y = y
        if(x<=3 and y <= 3):
            raise ValueError("Grid too small")
        if(x>self.__X_MAX_LENGHT or y>self.__Y_MAX_LENGHT-1):
            raise ValueError("Grid too big")
        self.sense.clear()
        for y_index in range(self.__Y_MAX_LENGHT-self.__grid_y,self.__Y_MAX_LENGHT):
            for x_index in range(0,self.__grid_x):
                self.sense.set_pixel(x_index,y_index,self.__GRAY)


    def draw_token(self, x: int, y: int, token) -> None:
        """
        Draws a game token at the specified position on the LED matrix.

        Args:
            x (int): The horizontal position (column) where the token should be drawn (0-based)
            y (int): The vertical position (row) where the token should be drawn (0-based).
                    Use -1 to draw in the selector row above the grid.
            token (GameToken): The type of token to draw (RED, YELLOW, or EMPTY)

        Raises:
            ValueError: If the token type is not recognized
            ValueError: If the position is outside the grid boundaries
        """
        if(y == -1):
            if(token == GameToken.RED):
                self.__draw_selector(x, self.__RED)
            elif(token == GameToken.YELLOW):
                self.__draw_selector(x, self.__YELLOW)
            elif(token == GameToken.EMPTY):
                self.__clear_selector(x)
            else:
                raise ValueError("Unknown token")
        else:
            if(x>=self.__grid_x or y >= self.__grid_y or x <= -1 or y <= -2):
                raise ValueError("Outbound of Grid")
            if(token == GameToken.RED):
                self.sense.set_pixel(x,y+(self.__Y_MAX_LENGHT-self.__grid_y),self.__RED)
            elif(token == GameToken.YELLOW):
                self.sense.set_pixel(x,y+(self.__Y_MAX_LENGHT-self.__grid_y),self.__YELLOW)
            elif(token == GameToken.EMPTY):
                self.sense.set_pixel(x,y+(self.__Y_MAX_LENGHT-self.__grid_y),self.__GRAY)
            else:
                raise ValueError("Unknown token")

    def draw_winner(self, token:GameToken) -> None:
        """
        Indicates the winner by lighting up the selector row with the winner's color.

        Args:
            token (GameToken): The winning player's token (RED or YELLOW)
        """
        for x in range(0,self.__grid_x):
            if(token == GameToken.RED):
                self.__draw_selector(x,self.__RED)
            elif(token == GameToken.YELLOW):
                self.__draw_selector(x,self.__YELLOW)

if __name__ == '__main__':
    sense = SenseHat()
    fc = DisplaySensehat(sense)
    fc.draw_grid(7,6)
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
    fc.draw_winner(GameToken.YELLOW)
    #print(fc.get_x_grid())
    #print(type(GameToken.RED))
    #print(GameToken.RED)
