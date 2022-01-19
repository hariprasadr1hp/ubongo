"""
Ubongo Game


How to input:
 pass the file to the program as follows:
    `python main.py --file={{input.txt}}`
"""

"""
The input file to this program is restricted to a specific format, as follows:

1) A new line between two 'matrix' inputs
2) Each matrix input starts with dimensions `row column` in the first line
3) Followed by its values row-wise
4) Space between each entries in the row
5) The first matrix is always the board matrix
6) In the board matrix, 0 and 1 represents fillable and non-fillable holes respectively
7) In the piece matrix, 0 and 1 represents void and non-void material 
8) no newline in the end of the file
9) no additional comments to the file

"""

import argparse
import sys
from typing import Dict, List, NamedTuple, Optional, Tuple
from pathlib import Path
import numpy as np
from src.libutil import GameError
from src.parse_input import parseUbongoInput
from src.ubongo_game import UbongoGame



def main():
    try:
        board, pieces = parseUbongoInput(fpath)
        game = UbongoGame(board, pieces)
        game.solve()
    except GameError as e:
        print(e)
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=False,
        metavar='',
        help='a .txt file with input, seperated by spaces for each piece input'
    )

    args = parser.parse_args()

    if args.input:
        try:
            fpath = Path(args.input)
        except TypeError:
            print("input file not found")
            sys.exit()

        if not fpath.exists():
            print("the file path doesn't exist, continuting with the default file")
            fpath = Path("./input.txt")

    else:
        fpath = Path("./input.txt")

    main()
