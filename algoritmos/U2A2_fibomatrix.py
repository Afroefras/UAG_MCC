from numpy import array


class FiboMatrix:
    def __init__(self) -> None:
        self.base = array([[0, 1], [1, 1]])

    def fibo_matrix(self, n: int) -> int:
        x = self.base.copy()
        for _ in range(n - 1):
            x = x @ self.base
        return x[-1][-1]

    def exp_square(self, x: int, n: float) -> int:
        if n % 2 == 0:
            return (x**2) ** (n / 2)
        else:
            return x * (x**2) ** ((n - 1) / 2)

    def exp_square_matrix(self, x: array, n: float) -> int:
        if n % 2 == 0:
            return (x @ x) ** (n / 2)
        else:
            return x * (x**2) ** ((n - 1) / 2)

    def recursive_exp_square(self, x, n: float) -> int:
        pass


fm = FiboMatrix()
# a = fm.fibo_matrix(500)
# print(a)
