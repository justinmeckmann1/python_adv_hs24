from sense_hat import SenseHat
from input_base import InputBase
from input_base import Keys
from enum import Enum


class InputJoystick(InputBase):
    """
    Input handler for sensehat applications using joystick input.
    """
    def __init__(self, p_sense:SenseHat):
        super().__init__()
        self.sense = p_sense

    def read_key(self) -> Enum:
        """
        Reads all joystick events and process the last one, if no event occured since the last call, will wait for one.

        Returns:
            Enum: The key code corresponding to the last joykstick movement.
        """
        event = self.sense.stick.wait_for_event()
        while not(event.action == "pressed" or event.action == "held"):
            event = self.sense.stick.wait_for_event()
        if event.direction == "up":
            return Keys.UP
        elif event.direction == "down":
            return Keys.DOWN
        elif event.direction == "left":
            return Keys.LEFT
        elif event.direction == "right":
            return Keys.RIGHT
        elif event.direction == "middle":
            return Keys.ENTER

if __name__ == '__main__':
    while True:
        sense = SenseHat()
        c = InputJoystick(sense)
        key = c.read_key()
        print(f"Taste: {key}, Type: {type(key)}")
        if key == Keys.ENTER:
            break
