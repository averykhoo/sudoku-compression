import itertools
import math
import random
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

"""
max possible options for a given element

   9 8 7   ? ? ?   3 2 1
   6 5 4  (12096)  3 2 1
   3 2 1   ? ? ?   3 2 1

   ? ? ?   ? ? ?   2 2 1
  (12096)  (448)   2 1 1    (limits for squares 2,4 determined via brute-force enumeration)
   ? ? ?   ? ? ?   1 1 1    (limit for square 5 determined via sampled enumeration)

   3 3 3   2 2 1   1 1 1
   2 2 2   2 1 1   1 1 1
   1 1 1   1 1 1   1 1 1
   
note:
    square 5 has different likelihoods, depending on squares 2 and 4
    Counter({400: 17743, 392: 5672, 448: 3913, 384: 2723, 432: 93})
    but it doesn't affect the overall bits of entropy, still under 76 bits
"""
POSSIBILITIES = [362880, 12096, 216, 12096, 448, 8, 216, 8, 1]
MAGIC_NUMBERS = [math.prod(POSSIBILITIES[i:]) for i in range(1, 9)]


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
    return ({square[0], square[3], square[6]},
            {square[1], square[4], square[7]},
            {square[2], square[5], square[8]})


@lru_cache(maxsize=362880)
def square_to_rows(square: Square) -> Tuple[Set[int], Set[int], Set[int]]:
    assert len(square) == 9
    return ({square[0], square[1], square[2]},
            {square[3], square[4], square[5]},
            {square[6], square[7], square[8]})


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


def squares_to_factors(squares: List[Square]) -> List[int]:
    def get_factor(square, squares_above, squares_left):
        for i, possibility in enumerate(all_possible_squares(constraint_squares_above=squares_above,
                                                             constraint_squares_left=squares_left)):
            if possibility == square:
                return i

    return [
        get_factor(squares[0], [], []),
        get_factor(squares[1], [], [squares[0]]),
        get_factor(squares[2], [], [squares[0], squares[1]]),
        get_factor(squares[3], [squares[0]], []),
        get_factor(squares[4], [squares[1]], [squares[3]]),
        get_factor(squares[5], [squares[2]], [squares[3], squares[4]]),
        get_factor(squares[6], [squares[0], squares[3]], []),
        get_factor(squares[7], [squares[1], squares[4]], [squares[6]]),
        get_factor(squares[8], [squares[2], squares[5]], [squares[6], squares[7]]),
    ]


def factors_to_number(factors: List[int]) -> int:
    assert len(factors) == 9
    assert factors[-1] == 0
    return sum(f * m for f, m in zip(factors[:-1], MAGIC_NUMBERS))


if __name__ == '__main__':
    board = '''
    8 3 5 4 1 6 9 2 7
    2 9 6 8 5 7 4 3 1
    4 1 7 2 9 3 6 5 8
    5 6 9 1 3 4 7 8 2
    1 2 3 6 7 8 5 4 9
    7 4 8 5 2 9 1 6 3
    6 5 2 7 8 1 3 9 4
    9 8 1 3 4 5 2 7 6
    3 7 4 9 6 2 8 1 5
    '''

    squares = board_to_squares(board)
    print(squares)
    factors = squares_to_factors(squares)
    print(factors)
    i = factors_to_number(factors)
    print(i)

if __name__ == '__main__':

    square_1 = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    square_2s = all_possible_squares(constraint_squares_left=[square_1])
    square_4s = all_possible_squares(constraint_squares_left=[square_1])

    # c2 = Counter()
    c3 = Counter()
    # c4 = Counter()
    c5 = Counter()
    c6 = Counter()
    c7 = Counter()
    c8 = Counter()
    c9 = Counter()

    # 1 2 3
    # 4 5 6
    # 7 8 9
    for _ in range(100):
        square_2 = random.choice(square_2s)

        square_3s = all_possible_squares(constraint_squares_left=[square_1, square_2])
        square_3 = random.choice(square_3s)
        c3[len(square_3s)] += 1

        square_4 = random.choice(square_4s)

        square_5s = all_possible_squares(constraint_squares_above=[square_2],
                                         constraint_squares_left=[square_4])
        square_5 = random.choice(square_5s)
        c5[len(square_5s)] += 1

        square_6s = all_possible_squares(constraint_squares_above=[square_3],
                                         constraint_squares_left=[square_4, square_5])
        square_6 = random.choice(square_6s)
        c6[len(square_6s)] += 1

        square_7s = all_possible_squares(constraint_squares_above=[square_1, square_4])
        square_7 = random.choice(square_7s)
        c7[len(square_7s)] += 1

        square_8s = all_possible_squares(constraint_squares_above=[square_2, square_5],
                                         constraint_squares_left=[square_7])

        n_8 = 0
        for square_8 in square_8s:

            square_9s = all_possible_squares(constraint_squares_above=[square_3, square_6],
                                             constraint_squares_left=[square_7, square_8])
            if square_9s:
                n_8 += 1
                assert len(square_9s) == 1

    # print('c1', c1)
    # print('c2', c2)
    print('c3', c3)
    # print('c4', c4)
    print('c5', c5)
    print('c6', c6)
    print('c7', c7)
    print('c8', c8)
    print('c9', c9)
