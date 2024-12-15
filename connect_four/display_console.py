from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase


class DisplayConsole(DisplayBase):
    """
    Console-based display implementation.

    Attributes:
        __STARTPOSITION_X (int): Starting X coordinate for the grid
        __STARTPOSITION_Y (int): Starting Y coordinate for the grid
        __SPACING_X (int): Horizontal spacing between grid cells
        __SPACING_Y (int): Vertical spacing between grid cells
    """
    __STARTPOSITION_X = 1
    __STARTPOSITION_Y = 1 
    __SPACING_X = 2
    __SPACING_Y = 1
    def __init__(self):
        """
        Initializes a new console display instance.
        """
        super().__init__()
        self.__grid_x = 0
        self.__grid_y = 0

    def __draw_selector(self, x:int) -> None:
        """
        Draws a selector indicator at the specified column.

        Args:
            x (int): The horizontal position (column) for the selector (0-based)
        """
        Ansi.gotoXY(x*(self.__SPACING_X+1)+2, 1)
        print("█"*self.__SPACING_X)

    def __clear_selector(self, x:int) -> None:
        """
        Clears the selector indicator at the specified column.

        Args:
            x (int): The horizontal position (column) to clear (0-based)
        """
        Ansi.gotoXY(x*(self.__SPACING_X+1)+2, 1)
        print("─"*self.__SPACING_X)

    def get_x_grid(self):
        """
        Returns the current grid width.

        Returns:
            int: The number of columns in the grid
        """
        return self.__grid_x
    
    def draw_grid(self, x:int, y:int) -> None:
        """
        Initializes and draws the game grid in the console.

        Args:
            x (int): Width of the grid (number of columns)
            y (int): Height of the grid (number of rows)

        Raises:
            ValueError: If grid dimensions are too small (< 3x3)
        """
        self.__grid_x = x
        self.__grid_y = y
        if(x<=3 and y <= 3):
            raise ValueError("Grid too small")
        Ansi.clear_screen()
        Ansi.reset()
        Ansi.gotoXY(self.__STARTPOSITION_X,self.__STARTPOSITION_Y)
        print("┌"+("─"*self.__SPACING_X+"┬") * (self.__grid_x-1)+"─"*self.__SPACING_X+"┐")
        for temp_index in range(self.__SPACING_Y):
            print("│"+(" "*self.__SPACING_X+"│") * (self.__grid_x-1)+" "*self.__SPACING_X+"│")
        for temp_index in range(self.__grid_y-1):
            print("├"+("─"*self.__SPACING_X+"┼") * (self.__grid_x-1)+"─"*self.__SPACING_X+"┤")
            for temp_index in range(self.__SPACING_Y):
                print("│"+(" "*self.__SPACING_X+"│") * (self.__grid_x-1)+" "*self.__SPACING_X+"│")
        print("└"+("─"*self.__SPACING_X+"┴") * (self.__grid_x-1)+"─"*self.__SPACING_X+"┘")
        Ansi.reset()

    def draw_token(self, x: int, y: int, token) -> None:
        """
        Draws a game token at the specified position on the console grid.

        Args:
            x (int): The horizontal position (column) where the token should be drawn (0-based)
            y (int): The vertical position (row) where the token should be drawn (0-based).
                    Use -1 to draw in the selector row above the grid.
            token (GameToken): The type of token to draw (RED, YELLOW, or EMPTY)

        Raises:
            ValueError: If the token type is not recognized
            ValueError: If the position is outside the grid boundaries
        """
        Ansi.reset()
        if(y == -1):
            if(token == GameToken.RED):
                Ansi.set_foreground(1,True)
                self.__draw_selector(x)
            elif(token == GameToken.YELLOW):
                Ansi.set_foreground(3,True)
                self.__draw_selector(x)
            elif(token == GameToken.EMPTY):
                self.__clear_selector(x)
            else:
                raise ValueError("Unknown token")
        else:
            if(x>=self.__grid_x or y >= self.__grid_y or x <= -1 or y <= -2):
                raise ValueError("Outbound of Grid")
            for tempIndex in range(self.__SPACING_Y):
                Ansi.gotoXY(((x)*(self.__SPACING_X+1)+2),((y)*(self.__SPACING_Y+1)+2+tempIndex))
                if(token == GameToken.RED):
                    Ansi.set_foreground(1,False)
                    print("█"*self.__SPACING_X)
                elif(token == GameToken.YELLOW):
                    Ansi.set_foreground(3,False)
                    print("█"*self.__SPACING_X)
                elif(token == GameToken.EMPTY):
                    print(" "*self.__SPACING_X)
                else:
                    raise ValueError("Unknown token")
                    break
        Ansi.reset()

    def draw_winner(self, token:GameToken) -> None:
        """
        Indicates the winner by highlighting the entire selector row.

        Args:
            token (GameToken): The winning player's token (RED or YELLOW)
        """
        Ansi.reset()
        for x in range(0,self.__grid_x):
            if(token == GameToken.RED):
                Ansi.set_foreground(1,True)
                self.__draw_selector(x)
            elif(token == GameToken.YELLOW):
                Ansi.set_foreground(3,True)
                self.__draw_selector(x)
        Ansi.reset()


"""
┌
┐
└
┘
├
┤
┼
─
│
┬
┴
█ 

https://de.wikipedia.org/wiki/Unicodeblock_Rahmenzeichnung
"""


if __name__ == '__main__':
    fc = DisplayConsole()
    fc.draw_grid(7,6)
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
    fc.draw_winner(GameToken.YELLOW)
    Ansi.gotoXY(1, 20)
    #print(fc.get_x_grid())
    #print(type(GameToken.RED))
    #print(GameToken.RED)
