from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase


class DisplayConsole(DisplayBase):
    __STARTPOSITION_X = 1
    __STARTPOSITION_Y = 1 
    __SPACING_X = 2
    __SPACING_Y = 1
    def __init__(self):
        super().__init__()
        self.__grid_x = 0
        self.__grid_y = 0

    def __draw_selector(self, x:int) -> None:
        Ansi.gotoXY(x*(self.__SPACING_X+1)+2, 1)
        print("█"*self.__SPACING_X)

    def __clear_selector(self, x:int) -> None:
        Ansi.gotoXY(x*(self.__SPACING_X+1)+2, 1)
        print("─"*self.__SPACING_X)

    def get_x_grid(self):
        return self.__grid_x
    
    def draw_grid(self, x:int, y:int) -> None:
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
