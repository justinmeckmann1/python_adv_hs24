from enum import Enum

class DropState(Enum):
    """
    Enum class representing different states after dropping a token in Connect Four.

    Attributes:
        DROP_OK (int): Indicates that the token was dropped successfully (value: 0)
        COLUMN_INVALID (int): Indicates that the selected column is invalid (value: 1)
        COLUMN_FULL (int): Indicates that the selected column is already full (value: 2)
        WRONG_PLAYER (int): Indicates that a player made a move when it wasn't their turn (value: 3)
    """
    DROP_OK = 0          # token dropped successfully
    COLUMN_INVALID = 1   # The selected column is invalid
    COLUMN_FULL = 2      # The selected column is already full
    WRONG_PLAYER = 3     # A player made a move that is not theirs
