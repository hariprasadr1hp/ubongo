from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from src.libutil import GameError
from src.board import Board
from src.piece import Piece

class UbongoGame:
    def __init__(self, board: Board, pieces: List[Piece]) -> None:
        self.board = board
        self.pieces = pieces
        self.gameInitialize()

    def gameInitialize(self):
        self.playboard = self.board.array
        self.brow, self.bcol = self.board.array.shape
        self.expected = np.zeros((self.brow, self.bcol), dtype=int)
        self.tile_positions: List[List[np.ndarray]] = []

    def printResult(self) -> None:
        print(self.playboard)

    def resetBoard(self) -> None:
        self.playboard = self.board.array

    def snapPosition(self, config: np.ndarray, position: np.ndarray) -> bool:
        """
        whether the position can tile in the cirrent configurartion

        algorithm: the element-wise product of the configuration and
        position matrix has to be zero. If non-zero, there is an overlap,
        in which case, the current position cannot tile to the board 
        """
        result = np.multiply(config, position)
        try:
            np.testing.assert_equal(result, self.expected)
            return True
        except AssertionError:
            return False

    def getPositions(self, config: np.ndarray, pattern: np.ndarray) -> List[np.ndarray]:
        """
        By sliding the piece kernel across both the rows and columns of the
        board/configuration matrix
        """
        prow, pcol = pattern.shape
        snap_positions: List[np.ndarray] = []

        for i in range(prow - self.brow + 1):
            for j in range(pcol - self.bcol + 1):
                position = pattern[i:i+self.brow, j:j+self.bcol]
                snapped = self.snapPosition(config, position)
                if snapped:
                    snap_positions.append(position)
        if snap_positions:
            return snap_positions
        raise GameError(
            "No way to snap this pattern in the given configurarion")

    def isSolved(self, playboard: np.ndarray) -> bool:
        # has zeros?
        if (np.vectorize(lambda x: True if x == 0 else False)(self.playboard)).any():
            # raise GameError("Not a solution. Has zeros in it")
            return False
        return True

    def solve(self) -> None:

        i: int = 0   # piece
        j: int = 0   # pattern
        k: int = 0   # position

        iflag = True
        jflag = True
        kflag = True

        # self.pieces.reverse()

        @dataclass
        class Attempt:
            piece: Piece
            pattern: int = 0
            position: int = 0
            array: Optional[np.ndarray] = None

        traverse_path: List[Attempt] = [
            Attempt(piece, 0, 0) for i, piece in enumerate(self.pieces)]
        
        tried: List[np.ndarray] = []
        
        

        while iflag:
            jflag = True
            kflag = True
            try:
                piece = self.pieces[i]
                while jflag:
                    kflag = True
                    try:
                        pattern = piece.padded_combinations[j]
                        try:
                            possible_positions = self.getPositions(self.playboard, pattern)
                            while kflag:
                                try:
                                    position = possible_positions[k]
                                    snapped = self.snapPosition(self.playboard, position)
                                    if snapped:
                                        tried.append(position)
                                        self.playboard = np.add(self.playboard, position)
                                        attempt = Attempt(piece, j, k, position)
                                        traverse_path.append(attempt)
                                        kflag = False
                                        jflag = False
                                        k = 0
                                        j = 0
                                        i += 1
                                        # print(attempt.pattern, attempt.position)
                                        # print()
                                        # print(self.playboard)
                                        # print()
                                    else:
                                        k += 1
                                except IndexError:
                                    j += 1
                                    k = 0
                        except GameError:
                            j += 1
                            k = 0
                    except IndexError:
                        # for each in tried:
                        #     print(each)
                        #     print()
                        # print("------------------------------------------------")
                        # print("------------------------------------------------")
                        self.playboard = np.subtract(self.playboard, tried.pop())
                        attempt = traverse_path.pop()
                        k = attempt.position + 1
                        j = attempt.pattern
                        jflag = False
                        kflag = False
                        i -= 1
            except IndexError:
                iflag = False
        
        print(self.playboard)

