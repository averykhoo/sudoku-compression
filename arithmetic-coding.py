import itertools
import re
from collections import Counter
from functools import lru_cache
from typing import Iterable
from typing import List
from typing import Sequence
from typing import Set
from typing import Tuple

# represents a 3x3 grid square, in this order:
# 1 2 3
# 4 5 6
# 7 8 9
Square = Tuple[int, ...]  # contains exactly 9 integers, but typechecking that correctly is hard


def board_to_squares(board: str) -> List[Square]:
    """
    parses sudoku board into integers (spaces don't matter), and validates sudoku board for correctness
    pulls out the values in each 3x3 squares, and returns them as tuples of integers

    >>> board_to_squares("7 2 4   8 6 5    1 9 3" \
                         "1 6 9   2 4 3    8 7 5" \
                         "3 8 5   1 9 7    2 4 6" \
                         "                      " \
                         "8 9 6   7 2 4    3 5 1" \
                         "2 7 3   9 5 1    6 8 4" \
                         "4 5 1   3 8 6    9 2 7" \
                         "                      " \
                         "5 4 2   6 3 9    7 1 8" \
                         "6 1 8   5 7 2    4 3 9" \
                         "9 3 7   4 1 8    5 6 2")
    [(7, 2, 4, 1, 6, 9, 3, 8, 5), (8, 6, 5, 2, 4, 3, 1, 9, 7), (1, 9, 3, 8, 7, 5, 2, 4, 6), (8, 9, 6, 2, 7, 3, 4, 5, 1), (7, 2, 4, 9, 5, 1, 3, 8, 6), (3, 5, 1, 6, 8, 4, 9, 2, 7), (5, 4, 2, 6, 1, 8, 9, 3, 7), (6, 3, 9, 5, 7, 2, 4, 1, 8), (7, 1, 8, 4, 3, 9, 5, 6, 2)]

    :param board: a string containing all the cells in a sudoku board (spaces don't matter)
    :return: 9 tuples, each containing the digits 1 through 9
    """

    # pull out the squares in this order:
    reference = '''
    1 1 1   2 2 2   3 3 3
    1 1 1   2 2 2   3 3 3
    1 1 1   2 2 2   3 3 3
    
    4 4 4   5 5 5   6 6 6
    4 4 4   5 5 5   6 6 6
    4 4 4   5 5 5   6 6 6
    
    7 7 7   8 8 8   9 9 9
    7 7 7   8 8 8   9 9 9
    7 7 7   8 8 8   9 9 9
    '''

    # parse reference and board
    reference_digits = [int(square_id) for square_id in re.findall(r'[1-9]', reference)]
    board_digits = [int(cell_value) for cell_value in re.findall(r'[1-9]', board)]

    # sanity check that we have the right quantity of cell values in the board
    assert len(reference_digits) == 9 * 9
    assert len(board_digits) == 9 * 9, f'invalid board: {repr(board)}'

    # validation helper to ensure the alldiff constraint is satisfied
    def validate_all_different(numbers: Sequence[int]):
        assert len(numbers) == 9
        assert len(set(numbers)) == 9

    # validate that each row contains the digits one through 9
    for row_id in range(9):
        validate_all_different(board_digits[row_id * 9:(row_id + 1) * 9])

    # validate that each column contains the digits one through 9
    for row_id in range(9):
        validate_all_different(board_digits[row_id::9])

    # group-by the cell values by their containing squares
    out = [[] for _ in range(9)]
    for square_id, cell_value in zip(reference_digits, board_digits):
        out[square_id - 1].append(cell_value)

    # validate that each square contains the digits one through 9
    for square in out:
        validate_all_different(square)

    # convert to tuples
    return [tuple(square) for square in out]


@lru_cache(maxsize=362880)
def square_to_cols(square: Square) -> Tuple[Set[int], Set[int], Set[int]]:
    assert len(square) == 9
    return {square[0], square[3], square[6]}, {square[1], square[4], square[7]}, {square[2], square[5], square[8]}


@lru_cache(maxsize=362880)
def square_to_rows(square: Square) -> Tuple[Set[int], Set[int], Set[int]]:
    assert len(square) == 9
    return {square[0], square[1], square[2]}, {square[3], square[4], square[5]}, {square[6], square[7], square[8]}


def all_possible_squares(*,
                         constraint_squares_above: Iterable[Square] = (),
                         constraint_squares_left: Iterable[Square] = (),
                         ) -> List[Square]:
    """
    returns a list of all possible squares that match the constraints given by squares above and to the left

    :param constraint_squares_above:
    :param constraint_squares_left:
    :return:
    """
    # collate column constraints
    constraint_col_1, constraint_col_2, constraint_col_3 = set(), set(), set()
    for square in constraint_squares_above:
        col_1, col_2, col_3 = square_to_cols(square)
        constraint_col_1.update(col_1)
        constraint_col_2.update(col_2)
        constraint_col_3.update(col_3)

    # collate row constraints
    constraint_row_1, constraint_row_2, constraint_row_3 = set(), set(), set()
    for square in constraint_squares_left:
        row_1, row_2, row_3 = square_to_rows(square)
        constraint_row_1.update(row_1)
        constraint_row_2.update(row_2)
        constraint_row_3.update(row_3)

    # try all possible squares
    out = []
    for square in itertools.permutations(range(1, 10)):
        if square[0] in constraint_col_1 or square[0] in constraint_row_1:
            continue
        if square[1] in constraint_col_2 or square[1] in constraint_row_1:
            continue
        if square[2] in constraint_col_3 or square[2] in constraint_row_1:
            continue
        if square[3] in constraint_col_1 or square[3] in constraint_row_2:
            continue
        if square[4] in constraint_col_2 or square[4] in constraint_row_2:
            continue
        if square[5] in constraint_col_3 or square[5] in constraint_row_2:
            continue
        if square[6] in constraint_col_1 or square[6] in constraint_row_3:
            continue
        if square[7] in constraint_col_2 or square[7] in constraint_row_3:
            continue
        if square[8] in constraint_col_3 or square[8] in constraint_row_3:
            continue
        out.append(square)

    return out



if __name__ == '__main__':
    from multiprocessing import Pool

    square_1 = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    square_2s = all_possible_squares(constraint_squares_left=[square_1])
    square_4s = all_possible_squares(constraint_squares_above=[square_1])

    print(len(square_2s))

    c = Counter()
    for i, square_2 in enumerate(square_2s[::20]):
        for j, square_4 in enumerate(square_4s[::20]):
            if (j + 1) % 100 == 0:
                print(i + 1, '/', len(square_2s)//20, square_2)
                print(c)
            square_5s = all_possible_squares(constraint_squares_above=[square_2], constraint_squares_left=[square_4])
            c[len(square_5s)] += 1

    print(c)
