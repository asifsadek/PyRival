import operator as op

transpose = lambda mat: list(map(list, zip(*mat)))

minor = lambda mat, i, j: [row[:j] + row[j + 1:] for row in (mat[:i]+mat[i + 1:])]

mat_add = lambda *mat: [[sum(elements) for elements in zip(*row)] for row in zip(*mat)]

mat_sub = lambda mat1, mat2: [[i - j for i, j in zip(*row)] for row in zip(mat1, mat2)]

mat_mul = lambda mat1, mat2: list(map(lambda row: list(map(lambda *column: sum(map(op.mul, row, column)), *mat2)), mat1))


def eye(m):
    identity = [[0]*m for _ in range(m)]
    for i, row in enumerate(identity):
        row[i] = 1

    return identity


def mat_pow(mat, power):
    if power < 0:
        return mat_pow(inverse(mat), -power)

    result = eye(len(mat))

    if power == 0:
        return result

    matrix = mat
    for i in '{0:b}'.format(power)[::-1]:
        if i == '1':
            result = mat_mul(result, matrix)
        matrix = mat_mul(matrix, matrix)

    return result


def det(mat):
    if len(mat) == 1:
        return mat[0][0]

    if len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

    return sum(pow(-1, i) * mat[0][i] * det(minor(mat, 0, i)) for i in range(len(mat)))


def inverse(m):
    determinant = det(m)
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]

    return transpose([[(pow(-1, i + j) * det(minor(m, i, j))) / determinant for j in range(len(m))] for i in range(len(m))])


linear_recurrence = lambda trans_matrix, known_values, k: mat_mul(mat_pow(trans_matrix, k), known_values)
