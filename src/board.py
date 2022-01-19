from src.libutil import sampleboard

class Board:
    """
    A board representation
    """

    def __init__(self, array=sampleboard()) -> None:
        self.array = array

    def __repr__(self) -> str:
        return str(self.array)

