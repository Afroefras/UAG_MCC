class Sudoku:
    def __init__(self) -> None:
        self.num = set(range(1, 10))

    def read_sudoku(self, sudoku: list) -> None:
        self.sudoku = sudoku
        self.n_chunks = len(self.sudoku)

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
    
    def is_row_legal(self, to_check: int, n_row: int) -> bool:
        n_row = n_row // 3
        all_rows = set(range(9))
        full_row = filter(lambda x: x // 3 == n_row, all_rows)

        for row_pos in full_row:
            if to_check in self.sudoku[row_pos]:
                return False

        return True
    
    def is_col_legal(self, to_check: int, n_col: int) -> bool:
        col_pos = n_col // 3
        chunks_pos = filter(lambda x: x % 3 == n_col, range(self.n_chunks))

        for chunk_pos in chunks_pos:
            chunk = self.sudoku[chunk_pos]
            print(chunk_pos, chunk, col_pos)
            if to_check == chunk[col_pos]:
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

a = sk.is_col_legal(4, 0)
print(a)