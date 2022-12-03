from train_curveadj_fuzzynet import CurveAdj
from matplotlib.pyplot import subplots

class PlotCurveAdj(CurveAdj):
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, range_considered, mutation_allowed: bool, **kwargs) -> None:
        super().__init__(population_size, tournament_size, n_generations, range_considered, mutation_allowed)

        self.fig, self.axes = subplots(nrows=1, ncols=2, **kwargs)
        self.func_x, self.func_y = [], []


    def plot_curves(self, i: int, **kwargs) -> None:
        self.axes[0].clear()
        self.axes[0].plot(self.actual_curve, color='blue')

        est_curve = self.curve_values(self.top_winners[i])
        self.axes[0].plot(est_curve, **kwargs)
        self.axes[0].set_ylim(top=max(self.actual_curve)*1.1)

        winner_func = self.function_to_eval(self.top_winners[i]).replace('"','')
        self.axes[0]
        self.axes[0].set_title(winner_func)


    def plot_error(self, i: int) -> None:
        min_error, max_error = self.top_errors[-1], self.top_errors[0]
        top_error = self.top_errors[i]

        self.func_x.append(i)
        self.func_y.append(top_error)

        self.axes[1].clear()
        
        error = f'Gen #{str(i+1).zfill(3)} error: {top_error:.2f}'
        self.axes[1].set_title(error)
        # self.axes[1].set_xlim([0, self.n_gen])
        self.axes[1].set_ylim([min_error*0.9, max_error])

        self.axes[1].plot(self.func_x, self.func_y, color='blue')


    def plot_curveadj(self, i, **kwargs) -> None:
        self.plot_curves(i, **kwargs)
        self.plot_error(i)
