from strenum import StrEnum

class GameToken(StrEnum):
    """
    Enum class representing the different game tokens in Connect Four.

    This class defines the possible tokens that can appear on the game board,
    including empty spaces and tokens for both players (Red and Yellow).

    Attributes:
        EMPTY (str): Represents an empty cell on the board (value: ' ')
        RED (str): Represents a red player's token (value: 'X')
        YELLOW (str): Represents a yellow player's token (value: '0')
    """
    EMPTY = ' '     # An empty token (placeholder)
    RED = 'X'       # Token for the red player
    YELLOW = '0'    # Token for the yellow player


if __name__ == '__main__':
    t = GameToken.RED
    st = str(t)
    print(f"GameToken {t}, Type: {type(t)}, Value: {t.value}, Type of Value: {type(t.value)}")
    print(f"GameToken {st}, Type: {type(st)}")
