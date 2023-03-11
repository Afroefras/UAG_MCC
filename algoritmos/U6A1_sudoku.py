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
            for j, y in enumerate(x):
                if j % 3 == 0:
                    to_print += "|"
                to_print += f" {y} "

            to_print += "|\n"
            if (i + 1) % 3 == 0:
                to_print += "-" * 30
                to_print += "\n"
        
        to_print = to_print.replace('0', ' ')
        return to_print

    def chain(self, *iterables):
        for it in iterables:
            for each in it:
                yield each

    def is_row_legal(self, to_check: int, n_row: int) -> bool:
        if to_check in self.sudoku[n_row]:
            return False
        
        return True

    def is_col_legal(self, to_check: int, n_col: int) -> bool:
        if to_check in {x[n_col] for x in self.sudoku}:
            return False
        
        return True

    def is_group_legal(self, to_check: int, n_row: int, n_col: int) -> bool:
        row_start = (n_row // 3) * 3
        row_end = row_start + 3

        rows = self.sudoku[row_start:row_end]

        col_start = (n_col // 3) * 3
        col_end = col_start + 3

        for row in rows:
            print(row[col_start:col_end])
            if to_check in row[col_start:col_end]:
                return False
            
        return True

    def solve_sudoku(self) -> None:
        pass


SUDOKU = [
    [5, 0, 0, 9, 1, 3, 7, 2, 0],
    [3, 0, 0, 0, 8, 0, 5, 0, 9],
    [0, 9, 0, 2, 5, 0, 0, 8, 0],
    [6, 8, 0, 4, 7, 0, 2, 3, 0],
    [0, 0, 9, 5, 0, 0, 4, 6, 0],
    [7, 0, 4, 0, 0, 0, 0, 0, 5],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 8, 9, 1, 6, 0, 0],
    [8, 5, 0, 7, 2, 0, 0, 0, 3],
]


sk = Sudoku()
sk.read_sudoku(SUDOKU)
print(sk)
