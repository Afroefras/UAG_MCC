from train_curveadj import CurveAdj
from matplotlib.pyplot import subplots

class PlotCurveAdj(CurveAdj):
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, range_considered, mutation_allowed: bool) -> None:
        super().__init__(population_size, tournament_size, n_generations, range_considered, mutation_allowed)

        self.fig, self.axes = subplots(nrows=1, ncols=2, figsize=(10,5))
        self.func_x, self.func_y = [], []


    def plot_curves(self, i: int, **kwargs) -> None:
        self.axes[0].clear()
        self.axes[0].plot(self.actual_curve, color='blue')

        est_curve = self.curve_values(self.winners[i])
        self.axes[0].plot(est_curve, **kwargs)

        self.axes[0].set_ylim(top=max(self.actual_curve)*1.1)
        self.axes[0].set_title(f'Estimated curve at gen #{i+1}')


    def plot_error(self, i: int) -> None:
        min_error, max_error = self.top_errors[self.n_gen-1], self.top_errors[0]
        top_error = self.top_errors[i]
        error = f'Error: {top_error:.2f}'

        self.func_x.append(i)
        self.func_y.append(top_error)

        self.axes[1].clear()

        self.axes[1].set_title(error)
        # self.axes[1].set_xlim([0, self.n_gen])
        self.axes[1].set_ylim([min_error*0.9, max_error])

        self.axes[1].plot(self.func_x, self.func_y, color='blue')


    def plot_curveadj(self, i, **kwargs) -> None:
        self.plot_curves(i, **kwargs)
        self.plot_error(i)
