from typing import List

import numpy as np

from src.libutil import GameError
from src.board import Board

class Piece:
    """
    Piece on the board. 'color' is the representation of the piece
    """
    def __new__(cls, array: np.ndarray, color: int, board: Board):
        # ensuring that the color code is greater than 1
        # 1 is assigned for the non-fillable hole in the board
        if color < 2:
            raise GameError("color value should be greater than 0")
        return object.__new__(cls)

    def __init__(self, array: np.ndarray, color: int, board: Board) -> None:
        self.array = array
        self.color = color
        self.board = board
        self.pieceInitialize()

    def pieceInitialize(self):
        self.combinations: List[np.ndarray] = []
        self.padded_combinations: List[np.ndarray] = []
        self.collectCombinations()

    def __repr__(self) -> str:
        return str(self.array)

    def paddify(self, arr: np.ndarray) -> np.ndarray:
        """
        padding on all four sides of the pattern, such that it can 
        go through all possible configuartions when doing the 
        element-wise dot product by sliding it though the 
        board/configuration
        """
        rowdiff = self.board.array.shape[0] - arr.shape[0]
        coldiff = self.board.array.shape[1] - arr.shape[1]
        
        if rowdiff < 0:
            raise GameError("Got a piece bigger than the dimensions of the board")

        if coldiff < 0:
            raise GameError("Got a piece bigger than the dimensions of the board")

        res = arr
        res = np.concatenate(
            (res, np.zeros((rowdiff, arr.shape[1]))),
            axis=0
        )
        res = np.concatenate(
            (np.zeros((rowdiff, arr.shape[1])), res),
            axis=0
        )
        res = np.concatenate(
            (res, np.zeros((2*rowdiff+arr.shape[0], coldiff))),
            axis=1
        )
        res = np.concatenate(
            (np.zeros((2*rowdiff+arr.shape[0], coldiff)), res),
            axis=1
        )
        return res

    def collectCombinations(self) -> None:
        """
        collecting all possible unique configuations, possible the piece
        """
        def appendIfNotExists(arr) -> None:
            """ checks whether the combination already exists"""
            flag: bool = True
            for each in self.combinations:
                try:
                    np.testing.assert_equal(arr, each)
                    flag = False
                    break
                except AssertionError:
                    pass
            if flag:
                self.combinations.append(arr)

        # rotations and reflections
        # for each of four rotations, there exists both
        # an up-down flip and a left-right flip
        # only the unique combinations are collected
        for i in range(4):
            rotated_arr = np.rot90(self.array, i)
            flipped_ud_arr = np.flipud(rotated_arr)
            flipped_lr_arr = np.fliplr(rotated_arr)

            appendIfNotExists(self.color * rotated_arr)
            appendIfNotExists(self.color * flipped_ud_arr)
            appendIfNotExists(self.color * flipped_lr_arr)

            self.padded_combinations = [
                self.paddify(i) for i in self.combinations]
