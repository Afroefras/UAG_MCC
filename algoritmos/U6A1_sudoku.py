from numpy import array


class Sudoku:
    def __init__(self) -> None:
        self.num = set(range(1, 10))

    def read_sudoku(self, sudoku: list) -> None:
        self.original = array(sudoku)
        self.sudoku = self.original.copy()

        self.n_chunks = len(self.sudoku)
        self.chunks = set(range(self.n_chunks))

    def __str__(self) -> str:
        to_print = ""
        for i, x in enumerate(self.sudoku):
            if i % 3 == 0:
                to_print += "\n| "
            if i % 9 == 0:
                to_print += "-" * 22
                to_print += "\n| "

            to_print += " ".join(map(str, x))
            to_print += " | "

        to_print += "\n  "
        to_print += "-" * 22

        to_print = to_print.replace("0", " ")
        return to_print

    def chain(self, *iterables):
        for it in iterables:
            for each in it:
                yield each

    def is_row_legal(self, to_check: int, n_row: int) -> bool:
        row_start = n_row * 3
        row_end = row_start + 3

        full_row = self.sudoku[row_start:row_end]
        full_row = self.chain(*full_row)

        if to_check in full_row:
            return False

        return True

    def is_col_legal(self, to_check: int, n_col: int) -> bool:
        col_pos = n_col // 3
        chunks_pos = filter(lambda x: x % 3 == col_pos, self.chunks)
        chunks = self.sudoku[list(chunks_pos)]

        col_mod = n_col % 3
        if to_check in {x[col_mod] for x in chunks}:
            return False

        return True

    def is_group_legal(self, to_check: int, n_row: int, n_col: int) -> bool:
        col_pos = n_col // 3
        chunks_pos = filter(lambda x: x % 3 == col_pos, self.chunks)
        chunks = self.sudoku[list(chunks_pos)]

        row_pos = n_row // 3
        row_start = row_pos * 3
        row_end = row_start + 3

        group = chunks[row_start:row_end]
        group = self.chain(*group)

        if to_check in group:
            return False
        
        return True

    def solve_sudoku(self) -> None:
        pass


SUDOKU = [
    [5, 0, 0],
    [9, 1, 3],
    [7, 2, 0],
    [3, 0, 0],
    [0, 8, 0],
    [5, 0, 9],
    [0, 9, 0],
    [2, 5, 0],
    [0, 8, 0],
    [6, 8, 0],
    [4, 7, 0],
    [2, 3, 0],
    [0, 0, 9],
    [5, 0, 0],
    [4, 6, 0],
    [7, 0, 4],
    [0, 0, 0],
    [0, 0, 5],
    [0, 2, 0],
    [0, 0, 0],
    [0, 0, 0],
    [4, 0, 0],
    [8, 9, 1],
    [6, 0, 0],
    [8, 5, 0],
    [7, 2, 0],
    [0, 0, 3],
]


sk = Sudoku()
sk.read_sudoku(SUDOKU)
print(sk)

for x in range(9):
    for y in range(9):
        a = sk.is_group_legal(1, x, y)
        if not a: print(f'{x}, {y}: {a}')
