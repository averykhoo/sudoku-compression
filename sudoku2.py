import itertools

inputs = """
9 7 3 5 8 1 4 2 6
5 2 6 4 7 3 1 9 8
1 8 4 2 9 6 7 5 3
2 4 7 8 6 5 3 1 9
3 9 8 1 2 4 6 7 5
6 5 1 7 3 9 8 4 2
8 1 9 3 4 2 5 6 7
7 6 5 9 1 8 2 3 4
4 3 2 6 5 7 9 8 1

7 2 4 8 6 5 1 9 3
1 6 9 2 4 3 8 7 5
3 8 5 1 9 7 2 4 6
8 9 6 7 2 4 3 5 1
2 7 3 9 5 1 6 8 4
4 5 1 3 8 6 9 2 7
5 4 2 6 3 9 7 1 8
6 1 8 5 7 2 4 3 9
9 3 7 4 1 8 5 6 2

1 5 7 6 8 2 3 4 9
4 3 2 5 1 9 6 8 7
6 9 8 3 4 7 2 5 1
8 2 5 4 7 6 1 9 3
7 1 3 9 2 8 4 6 5
9 6 4 1 3 5 7 2 8
5 4 1 2 9 3 8 7 6
2 8 9 7 6 1 5 3 4
3 7 6 8 5 4 9 1 2

8 3 5 4 1 6 9 2 7
2 9 6 8 5 7 4 3 1
4 1 7 2 9 3 6 5 8
5 6 9 1 3 4 7 8 2
1 2 3 6 7 8 5 4 9
7 4 8 5 2 9 1 6 3
6 5 2 7 8 1 3 9 4
9 8 1 3 4 5 2 7 6
3 7 4 9 6 2 8 1 5

6 2 8 4 5 1 7 9 3
5 9 4 7 3 2 6 8 1
7 1 3 6 8 9 5 4 2
2 4 7 3 1 5 8 6 9
9 6 1 8 2 7 3 5 4
3 8 5 9 6 4 2 1 7
1 5 6 2 4 3 9 7 8
4 3 9 5 7 8 1 2 6
8 7 2 1 9 6 4 3 5

1 2 3 4 5 6 7 8 9
4 5 6 7 8 9 1 2 3
7 8 9 1 2 3 4 5 6
2 1 4 3 6 5 8 9 7
3 6 5 8 9 7 2 1 4
8 9 7 2 1 4 3 6 5
5 3 1 6 4 8 9 7 2
6 4 8 9 7 2 5 3 1
9 7 2 5 3 1 6 4 8

1 4 5 7 9 2 8 3 6
3 7 6 5 8 4 1 9 2
2 9 8 3 6 1 7 5 4
7 3 1 9 2 8 6 4 5
8 5 9 6 4 7 3 2 1
4 6 2 1 3 5 9 8 7
6 2 4 8 7 3 5 1 9
5 8 7 4 1 9 2 6 3
9 1 3 2 5 6 4 7 8

5 2 7 4 1 6 9 3 8
8 6 4 3 2 9 1 5 7
1 3 9 5 7 8 6 4 2
2 9 1 8 5 4 3 7 6
3 4 8 6 9 7 5 2 1
6 7 5 1 3 2 4 8 9
7 1 2 9 4 5 8 6 3
4 8 3 2 6 1 7 9 5
9 5 6 7 8 3 2 1 4

2 4 6 7 1 3 9 8 5
1 8 5 4 9 6 7 3 2
9 3 7 8 2 5 1 4 6
6 7 8 5 4 2 3 9 1
4 9 3 1 6 8 2 5 7
5 1 2 3 7 9 4 6 8
8 2 4 9 5 7 6 1 3
7 5 9 6 3 1 8 2 4
3 6 1 2 8 4 5 7 9

8 6 1 2 9 4 5 7 3
4 7 5 3 1 8 6 9 2
3 9 2 5 6 7 8 1 4
2 3 6 4 5 9 7 8 1
1 5 4 7 8 3 2 6 9
9 8 7 6 2 1 3 4 5
5 2 9 1 7 6 4 3 8
6 4 8 9 3 2 1 5 7
7 1 3 8 4 5 9 2 6
""".strip().split('\n\n')


def print_sudoku(m):
    for k in m:
        print(' '.join(str(i) for i in k))


def potential_squares(u1, u2, u3, l1, l2, l3):
    """
    returns generator of possible squares given lists of digits above and below

           u1 u2 u3
           |  |  |
    l1 --  a  b  c
    l2 --  d  e  f
    l3 --  g  h  i

    if no items exist the empty list must be given
    """
    for a, b, c, d, e, f, g, h, i in itertools.permutations(range(1, 10)):
        if a not in u1 and a not in l1 and b not in u2 and b not in l1 and c not in u3 and c not in l1 and d not in u1 and d not in l2 and e not in u2 and e not in l2 and f not in u3 and f not in l2 and g not in u1 and g not in l3 and h not in u2 and h not in l3 and i not in u3 and i not in l3:
            yield (a, b, c, d, e, f, g, h, i)


def board_to_squares(board):
    """
    finds 9 squares in a 9x9 board in this order:
    1 1 1 2 2 2 3 3 3
    1 1 1 2 2 2 3 3 3
    1 1 1 2 2 2 3 3 3
    4 4 4 5 5 5 6 6 6
    4 4 4 5 5 5 6 6 6
    4 4 4 5 5 5 6 6 6
    7 7 7 8 8 8 9 9 9
    7 7 7 8 8 8 9 9 9
    7 7 7 8 8 8 9 9 9

    returns tuple for each square as follows:
    a b c
    d e f   -->  (a,b,c,d,e,f,g,h,i)
    g h i
    """
    labels = [[3 * i + 1] * 3 + [3 * i + 2] * 3 + [3 * i + 3] * 3 for i in [0, 0, 0, 1, 1, 1, 2, 2, 2]]
    labelled_board = list(zip(sum(board, []), sum(labels, [])))
    return [tuple(a for a, b in labelled_board if b == sq) for sq in range(1, 10)]


def squares_to_board(squares):
    """
    inverse of above
    """
    board = [[i // 3 * 27 + i % 3 * 3 + j // 3 * 9 + j % 3 for j in range(9)] for i in range(9)]
    flattened = sum([list(square) for square in squares], [])
    for i in range(9):
        for j in range(9):
            board[i][j] = flattened[board[i][j]]
    return board


def sum_rows(*squares):
    """
    takes tuples for squares and returns lists corresponding to the rows:
    l1 -- a b c   j k l
    l2 -- d e f   m n o  ...
    l3 -- g h i   p q r
    """
    l1 = []
    l2 = []
    l3 = []
    if len(squares):
        for a, b, c, d, e, f, g, h, i in squares:
            l1 += [a, b, c]
            l2 += [d, e, f]
            l3 += [g, h, i]
        return l1, l2, l3
    return [], [], []


def sum_cols(*squares):
    """
    takes tuples for squares and returns lists corresponding to the rows:

    u1 u2 u3
    |  |  |
    a  b  c
    d  e  f
    g  h  i

    j  k  l
    m  n  o
    p  q  r

      ...

    """
    u1 = []
    u2 = []
    u3 = []
    if len(squares):
        for a, b, c, d, e, f, g, h, i in squares:
            u1 += [a, d, g]
            u2 += [b, e, h]
            u3 += [c, f, i]
        return u1, u2, u3
    return [], [], []


def base95(A):
    if type(A) is int:
        s = ''
        while A > 0:
            s += chr(32 + A % 95)
            A //= 95
        return s
    if type(A) is str:
        return sum((ord(c) - 32) * (95 ** i) for i, c in enumerate(A))


"""
dependencies: every square as labelled
1 2 3
4 5 6
7 8 9
is dependent on those above and to the left

in a dictionary, it is:
square: ([above],[left])
"""
dependencies = {1: ([], []), 2: ([], [1]), 3: ([], [1, 2]), 4: ([1], []), 5: ([2], [4]), 6: ([3], [4, 5]),
                7: ([1, 4], []), 8: ([2, 5], [7]), 9: ([3, 6], [7, 8])}
"""
max possible options for a given element

  9 8 7   ? ? ?   3 2 1
  6 5 4  (12096)  3 2 1
  3 2 1   ? ? ?   3 2 1

  ? ? ?   ? ? ?   2 2 1
 (12096)  (420)   2 1 1    (limits for squares 2,4 determined experimentally)
  ? ? ?   ? ? ?   1 1 1    (limit for square 5 is a pessimistic guess, might be wrong)

  3 3 3   2 2 1   1 1 1
  2 2 2   2 1 1   1 1 1
  1 1 1   1 1 1   1 1 1
"""
possibilities = [362880, 12096, 216, 12096, 420, 8, 216, 8, 1]


def factorize_sudoku(board):
    squares = board_to_squares(board)
    factors = []

    for label in range(1, 10):
        above, left = dependencies[label]
        u1, u2, u3 = sum_cols(*[sq for i, sq in enumerate(squares) if i + 1 in above])
        l1, l2, l3 = sum_rows(*[sq for i, sq in enumerate(squares) if i + 1 in left])
        for i, k in enumerate(potential_squares(u1, u2, u3, l1, l2, l3)):
            if k == squares[label - 1]:
                factors.append(i)
                continue
    return factors


def unfactorize_sudoku(factors):
    squares = []
    for label in range(1, 10):
        factor = factors[label - 1]
        above, left = dependencies[label]
        u1, u2, u3 = sum_cols(*[sq for i, sq in enumerate(squares) if i + 1 in above])
        l1, l2, l3 = sum_rows(*[sq for i, sq in enumerate(squares) if i + 1 in left])
        for i, k in enumerate(potential_squares(u1, u2, u3, l1, l2, l3)):
            if i == factor:
                squares.append(k)
                continue
    return squares


#
#
# ENCODE SUDOKU -> TEXT
#
#



sudoku_strings = []
for sudoku in inputs:
    board = [[int(x) for x in line.split()] for line in sudoku.strip().split('\n')]
    print_sudoku(board)
    factors = factorize_sudoku(board)

    i = 0
    for item, modulus in zip(factors, possibilities):
        i *= modulus
        i += item

    sudoku_strings.append(base95(i))
    print('integral representation:', i)
    print('bits of entropy:', i.bit_length())
    print('base95 representation:', sudoku_strings[-1])
    print()

print('overall output:', sudoku_strings)
print('total length:', len(''.join(sudoku_strings)))
print()


#
#
#  DECODE TEXT -> SUDOKU
#
#


for sudoku_string in sudoku_strings:
    print('from:', sudoku_string)

    i = base95(sudoku_string)
    retrieved = []
    for base in possibilities[::-1]:
        retrieved.append(i % base)
        i //= base

    squares = unfactorize_sudoku(retrieved[::-1])
    print_sudoku(squares_to_board(squares))
    print()
