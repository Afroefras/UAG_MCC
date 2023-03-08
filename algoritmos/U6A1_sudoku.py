class Sudoku:
    def __init__(self) -> None:
        self.num = set(range(1, 10))

    def read_sudoku(self, sudoku: list) -> None:
        self.sudoku = sudoku

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
