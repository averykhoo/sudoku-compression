# http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/


def hyper_phi(dim):
    """
    a high-dimensional golden ratio
    known as generalized fibonacci sequence / delayed fibonacci sequence
    satisfies the equation: x ** (dim + 1) == x + 1

    adapted from: http://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/
    hyper_phi(1) = 1.61803398874989484820458683436563
    hyper_phi(2) = 1.32471795724474602596090885447809

    :param dim:
    :return:
    """
    _x = 1.0
    _p = 1.0 / (dim + 1)
    for _ in range(40):
        # _x = _x - (pow(_x, d + 1) - _x - 1) / ((d + 1) * pow(_x, d) - 1)
        _x = (_x + 1) ** _p
    return _x


def get_points(n, dim=2, seed=0.5):
    """
    voronoi of 2d output produces hexagons for any n = [
        1,
        12,
        151,
        1897,
        23833,
        299426,
        4,
        49,
        616,
        7739,
        97229,
        1221537,
    ]
    :param n: number of points
    :param dim: dimension
    :param seed: any real number, typically 0, better 0.5
    :return: array of points
    """
    g = hyper_phi(dim)
    alpha = [0.0] * dim
    for j in range(dim):
        alpha[j] = pow(1.0 / g, j + 1) % 1

    points = [[0.0] * dim for _ in range(n)]
    points[0] = [a + seed for a in alpha]
    for i in range(n - 1):
        points[i + 1] = [p + a for p, a in zip(points[i], alpha)]

    return [[p % 1 for p in row] for row in points]


if __name__ == '__main__':
    tmp = dict()
    for x, y in get_points(999, 2):
        x = int(x * 9)
        y = int(y * 9)
        tmp.setdefault((x, y), len(tmp) + 1)
        if len(tmp) == 81:
            break

    print(tmp)
    tmp2 = [[0] * 9 for _ in range(9)]
    for (x, y), i in tmp.items():
        tmp2[x][y] = i
    print(tmp2)

    for row in tmp2:
        print('\t'.join(map(str, row)))

    tmp3 = []
    for k, v in tmp.items():
        tmp3.append(k)
        assert len(tmp3) == v
    print(tmp3)

    tmp4 = [None] * 81
    found = 0
    for x in get_points(999, 1):
        x = int(x[0] * 81)
        assert 0 <= x < 81
        if tmp4[x] is None:
            found += 1
            tmp4[x] = found
        if found == 81:
            break
    print(tmp4)
