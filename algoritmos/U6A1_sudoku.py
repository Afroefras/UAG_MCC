from numpy import array


class Sudoku:
    def __init__(self) -> None:
        self.num = set(range(1, 10))

    def read_sudoku(self, sudoku: list) -> None:
        self.original = array(sudoku)
        self.sudoku = self.original.copy()

    def __str__(self, sudoku: list) -> str:
        to_print = "-" * 30
        to_print += "\n"

        for i, x in enumerate(sudoku):
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

    def is_row(self, to_check: int, i: int) -> bool:
        row_start = (i // 9) * 9
        row_end = row_start + 9

        if to_check in self.sudoku[row_start:row_end]:
            return False

        return True

    def is_col(self, to_check: int, i: int) -> bool:
        col_start = i % 9
        if to_check in self.sudoku[col_start::9]:
            return False

        return True

    def is_group(self, to_check: int, i: int) -> bool:
        row_start = (i // 27) * 27
        row_end = row_start + 27
        group_rows = self.sudoku[row_start:row_end]

        col_start = ((i % 9) // 3) * 3
        group = set(group_rows[col_start::9])
        group.update(group_rows[col_start + 1 :: 9])
        group.update(group_rows[col_start + 2 :: 9])

        if to_check in group:
            return False

        return True

    def is_legal(self, x: int, i: int) -> bool:
        return self.is_group(x, i) and self.is_row(x, i) and self.is_col(x, i)

    def solve_sudoku(self, i: int) -> None:
        a = f"Start i={i}: "

        next_i = i + 1
        if self.original[i] == 0:
            for x in self.num:
                legal = self.is_legal(x, i)
                if legal and x > self.sudoku[i]:
                    a += f"{x} assigned i={i} it was {self.sudoku[i]}, "
                    print(a)
                    self.sudoku[i] = x
                    self.solve_sudoku(next_i)
                    print(self.__str__(self.sudoku))

        else:
            self.solve_sudoku(next_i)

        print(a)


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

# SUDOKU = [
#     6,9,0,0,0,0,7,0,0,
#     0,0,0,0,9,6,0,0,0,
#     0,8,0,7,5,3,0,9,0,
#     0,2,0,3,7,4,5,6,1,
#     3,6,0,0,0,5,0,2,0,
#     0,0,0,9,6,0,3,7,8,
#     0,0,6,0,3,1,0,8,4,
#     0,4,5,8,0,7,6,0,0,
#     0,0,0,0,0,0,0,5,7,
# ]

sk = Sudoku()
sk.read_sudoku(SUDOKU)
a = sk.__str__(sk.original)
print(a)

a = sk.solve_sudoku(0)
print(a)
