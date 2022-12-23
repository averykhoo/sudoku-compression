from sudoku_csp_solver import solve_sudoku
from quasirandom import    get_points

tmp = dict()
for x, y in get_points(999, 2):
    x = int(x * 9)
    y = int(y * 9)
    tmp.setdefault((x, y), len(tmp) + 1)
    if len(tmp) == 81:
        break

tmp2 = [[0] * 9 for _ in range(9)]
for (x, y), i in tmp.items():
    tmp2[x][y] = i
for row in tmp2:
    print('\t'.join(map(str, row)))

# order in which each cell is to be added
MAGIC_ORDERING = [x for sublist in tmp2 for x in sublist]

# invert the list to get the cells to add in order
MAGIC_INVERSE = [0] * 81
for i, x in enumerate(MAGIC_ORDERING):
    MAGIC_INVERSE[x - 1] = i + 1

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

if __name__ == '__main__':

    for puzzle in inputs:
        #
        # puzzle = '''
        # 9 7 3 5 8 1 4 2 6
        # 5 2 6 4 7 3 1 9 8
        # 1 8 4 2 9 6 7 5 3
        # 2 4 7 8 6 5 3 1 9
        # 3 9 8 1 2 4 6 7 5
        # 6 5 1 7 3 9 8 4 2
        # 8 1 9 3 4 2 5 6 7
        # 7 6 5 9 1 8 2 3 4
        # 4 3 2 6 5 7 9 8 1
        # '''.split()
        puzzle = puzzle.split()
        tmp = ['*'] * 81

        for i, n in enumerate(MAGIC_INVERSE):
            tmp[n - 1] = puzzle[n - 1]

            # sudoku puzzles with fewer than this number of vars is unsolvable
            if i < 19:
                continue
            # print(i)
            # print(''.join(tmp))
            solution = solve_sudoku(''.join(tmp))
            # print(solution)
            # print(''.join(puzzle))
            # print('-' * 100)
            if solution == ''.join(puzzle):
                print(f'solved, needed {i + 1} vars')
                break
