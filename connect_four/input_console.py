try: import msvcrt # skip for entry on raspberry, because msvcrt is not avaliable for unix
except ModuleNotFoundError:
     pass
from input_base import InputBase
from input_base import Keys
from enum import Enum


class InputConsole(InputBase):
    """
    Input handler for console applications using keyboard input.
    """

    def key_pressed(self) -> bool:
        """
        Check if a key has been pressed.

        Returns:
            bool: True if a key is pressed, False otherwise.
        """
        return msvcrt.kbhit()

    def read_key(self) -> Enum:
        """
        Read a key from the console and return its corresponding key code.

        Returns:
            Enum: The key code corresponding to the pressed key.
        """
        key = msvcrt.getch()

        if key in (b'\xe0', b'\x00'):  # Special keys (arrow keys send two bytes)
            key = msvcrt.getch()  # Get the second byte for direction
            if key == b'H':
                    return Keys.UP
            elif key == b'P':
                return Keys.DOWN
            elif key == b'K':
                    return Keys.LEFT
            elif key ==  b'M':
                    return Keys.RIGHT
            else:
                    return Keys.UNKNOWN
        else:
            if key == b'\r':
                return Keys.ENTER
            elif key == b'\x1b':
                    return Keys.ESC
            elif key == b'\03':  # Ctrl+C
                raise KeyboardInterrupt()  # Trigger a KeyboardInterrupt
            else:
                return Keys.UNKNOWN


if __name__ == '__main__':
    while True:
        c = InputConsole()
        key = c.read_key()
        print(f"Taste: {key}, Type: {type(key)}")
        if key == Keys.ENTER:
            print("Enter")
        if (key == Keys.ESC):  # Abort with ESC
            break
