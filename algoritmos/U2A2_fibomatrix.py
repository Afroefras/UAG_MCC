from time import time
from numpy import array, arange
from matplotlib.pyplot import plot, title, legend, show


class FiboMatrix:
    def __init__(self) -> None:
        self.base = array([[0, 1], [1, 1]])
        self.base_square = self.base @ self.base

    def fibomatrix(self, n: int) -> int:
        x = self.base.copy()

        for _ in range(n - 1):
            x = x @ self.base

        return x

    def quick_exp(self, n: int) -> int:
        if n <= 1:
            return 1

        x = self.base_square.copy()

        if n % 2 != 0:
            n -= 1
            x = x @ self.base

        for _ in range(n // 2 - 1):
            x = x @ self.base_square

        return x


class GetComplexity:
    def __init__(self) -> None:
        pass

    def event_time(self, func_to_run, x) -> float:
        start = time()
        func_to_run(x)
        end = time()

        return end - start

    def function_time(self, n_events: int, func_to_run) -> tuple:
        x = arange(n_events)
        y = [self.event_time(func_to_run, a) for a in x]

        return x, y


class PlotFiboMatrix(FiboMatrix, GetComplexity):
    def __init__(self) -> None:
        super().__init__()

    def plot_fibomatrix(self, n_events: int) -> None:
        f_x, f_y = self.function_time(n_events, self.fibomatrix)
        q_x, q_y = self.function_time(n_events, self.quick_exp)

        plot(f_x, f_y, color="#4C64A4")
        plot(q_x, q_y, color="#D86A6A", linestyle="dashed")
        title("Fibonacci")
        legend(["matricial", "exp. rápida"])
        show()


pfm = PlotFiboMatrix()

pfm.plot_fibomatrix(n_events=10000)
