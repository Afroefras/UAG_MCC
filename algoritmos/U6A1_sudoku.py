from numpy import array


class Sudoku:
    def __init__(self) -> None:
        self.num = set(range(1, 10))

    def read_sudoku(self, sudoku: list) -> None:
        self.original = array(sudoku)
        self.sudoku = self.original.copy()

    def __str__(self) -> str:
        to_print = "-" * 30
        to_print += "\n"

        for i, x in enumerate(self.sudoku):
            i += 1

            if i % 3 == 1:
                to_print += "|"

            to_print += f" {x} "

            if i % 9 == 0:
                to_print += "|\n"

            if i % 27 == 0:
                to_print += "-" * 30
                to_print += "\n"

        to_print = to_print.replace("0", " ")
        return to_print

    def is_row_legal(self, to_check: int, i: int) -> bool:
        row_start = (i // 9) * 9
        row_end = row_start + 9

        if to_check in self.sudoku[row_start:row_end]:
            return False

        return True

    def is_col_legal(self, to_check: int, i: int) -> bool:
        start = i // 9
        if to_check in self.sudoku[start::9]:
            return False

        return True

    def is_group_legal(self, to_check: int, n_row: int, n_col: int) -> bool:
        row_start = (n_row // 3) * 3
        row_end = row_start + 3

        rows = self.sudoku[row_start:row_end]

        col_start = (n_col // 3) * 3
        col_end = col_start + 3

        for row in rows:
            if to_check in row[col_start:col_end]:
                return False

        return True

    def solve_sudoku(self, i: int, j: int) -> None:
        if i == j == 9 * 9:
            return self.__str__()

        a = i
        b = j + 1
        if b > 8:
            a += 1
            b = 0

        print(f"For i={i}, j={j} then a={a}, b={b}")

        if self.original[i, j] == 0:
            for x in self.num:

                row = self.is_row_legal(x, i)
                col = self.is_col_legal(x, j)
                group = self.is_group_legal(x, i, j)

                if row and col and group:
                    self.sudoku[i, j] = x
                    print(self.__str__())

                    self.solve_sudoku(a, b)
        else:
            self.solve_sudoku(a, b)


SUDOKU = [
    5,
    0,
    0,
    9,
    1,
    3,
    7,
    2,
    0,
    3,
    0,
    0,
    0,
    8,
    0,
    5,
    0,
    9,
    0,
    9,
    0,
    2,
    5,
    0,
    0,
    8,
    0,
    6,
    8,
    0,
    4,
    7,
    0,
    2,
    3,
    0,
    0,
    0,
    9,
    5,
    0,
    0,
    4,
    6,
    0,
    7,
    0,
    4,
    0,
    0,
    0,
    0,
    0,
    5,
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    4,
    0,
    0,
    8,
    9,
    1,
    6,
    0,
    0,
    8,
    5,
    0,
    7,
    2,
    0,
    0,
    0,
    3,
]


sk = Sudoku()
sk.read_sudoku(SUDOKU)
print(sk)

for i in range(0, 90, 10):
    a = sk.is_col_legal(4, i)
    print(a)
# sk.solve_sudoku(0, 0)
