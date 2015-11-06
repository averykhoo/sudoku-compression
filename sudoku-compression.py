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

for input in inputs:

    # write out groups of digits
    r = range(9)
    g1 = [range(i * 9, i * 9 + 9) for i in r]
    g2 = [[i / 3 * 27 + i % 3 * 3 + j / 3 * 9 + j % 3 for j in r] for i in r]
    groups = g1 + zip(*g1) + g2

    # # print groups
    # for i, s in enumerate(groups):
    #     if i and not i % 9:
    #         print ''
    #     print '\t'.join(str(c) for c in s)

    # no point trying another order, sudoku is invariant under possible transforms
    board = [int(x) for x in input.split()]

    # convert sudoku to int
    acc = 0
    m = 1
    for i in sum(g1, []):
        # options for this slot
        allowed = set(xrange(1, 10))
        for s in groups:
            if i in s:
                for j in s:
                    if j < i:
                        allowed.discard(board[j])
        allowed = sorted(allowed)
        acc += m * allowed.index(board[i])
        # print i, board[i], allowed, m, acc
        m *= len(allowed)

    print 'bits of entropy:', acc.bit_length()
    # convert int to base 95 string
    s = ''
    while acc:
        s += chr(32 + acc % 95)
        acc /= 95
    print s


    # convert base 95 string to int
    acc = sum((ord(c) - 32) * 95 ** i for i, c in enumerate(s))

    board = []
    for i in xrange(81):
        allowed = set(xrange(1, 10))
        for s in groups:
            if i in s:
                for j in s:
                    if j < i:
                        allowed.discard(board[j])
        allowed = sorted(allowed)
        board += [allowed[acc % len(allowed)]]
        acc /= len(allowed)

    for i in xrange(9):
        print ' '.join(str(x) for x in board[i * 9:i * 9 + 9])
    print ''
