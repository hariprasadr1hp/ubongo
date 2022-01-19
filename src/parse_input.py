from typing import List, Tuple
from pathlib import Path

import numpy as np

from src.board import Board
from src.piece import Piece


def parseUbongoInput(filepath: Path) -> Tuple[Board, List[Piece]]:
    """
    parsing the input file and creating board and piece object instances
    """
    # considering no trailing whitespaces
    arrays: List[np.ndarray] = []
    temp_array: np.ndarray

    with open(filepath, 'r') as f:
        while True:
            try:
                shape = np.array(next(f).rstrip("\n").split(" "), dtype=int)

                temp_array = np.array([
                    next(f).rstrip("\n").split(" ") for _ in range(shape[0])
                ], dtype=int)

                arrays.append(temp_array)

                if next(f) == "\n":
                    pass

            except StopIteration:
                break

    board: Board = Board(arrays[0])
    pieces: List[Piece] = [
        Piece(each, color=i+2, board=board) for i, each in enumerate(arrays[1:])
    ]

    return board, pieces
