from sense_hat import SenseHat
from game_token import GameToken
from display_base import DisplayBase


class DisplaySensehat(DisplayBase):
    __CLEAR = (0,0,0)
    __GRAY = (50,50,50)
    __RED = (255,0,0)
    __YELLOW = (255,255,0)
    __X_MAX_LENGHT = 8
    __Y_MAX_LENGHT = 8
    def __init__(self, p_sense:SenseHat):
        super().__init__()
        self.__grid_x = 0
        self.__grid_y = 0
        self.sense = p_sense

    def __draw_selector(self, x:int, p_color) -> None:
        self.sense.set_pixel(x,(self.__Y_MAX_LENGHT-self.__grid_y)-1,p_color)

    def __clear_selector(self, x:int) -> None:
        self.sense.set_pixel(x,(self.__Y_MAX_LENGHT-self.__grid_y)-1,self.__CLEAR)

    def get_x_grid(self):
        return self.__grid_x
    
    def draw_grid(self, x:int, y:int) -> None:
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


if __name__ == '__main__':
    sense = SenseHat()
    fc = DisplaySensehat(sense)
    fc.draw_grid(7,6)
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
    #print(fc.get_x_grid())
    #print(type(GameToken.RED))
    #print(GameToken.RED)
