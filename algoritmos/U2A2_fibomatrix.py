from time import time
from numpy import array, arange, eye
from matplotlib.pyplot import plot, title, legend, show, xlabel, ylabel


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
            return self.base

        x = self.base_square.copy()

        if n % 2 != 0:
            n -= 1
            x = x @ self.base

        for _ in range(n // 2 - 1):
            x = x @ self.base_square

        return x

    def fiboquick(self, x: array, n: int) -> int:
        if n > 1:
            a = x @ x
            b = eye((2))

            if n % 2 != 0:
                n -= 1
                b = x.copy()

            n /= 2
            x = b @ self.fiboquick(a, n)

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
        fq_x, fq_y = self.function_time(
            n_events, lambda x: self.fiboquick(self.base, x)
        )

        plot(f_x, f_y, color="#4C64A4")
        plot(q_x, q_y, color="#D86A6A")
        plot(fq_x, fq_y, color="#DEC05F", linestyle="dashed")

        legend(["matricial", "exp. rápida lineal", "exp. rápida recursiva"])
        title("Fibonacci algorithms")
        xlabel("# of events")
        ylabel("Seconds")
        show()


pfm = PlotFiboMatrix()

pfm.plot_fibomatrix(n_events=200)
