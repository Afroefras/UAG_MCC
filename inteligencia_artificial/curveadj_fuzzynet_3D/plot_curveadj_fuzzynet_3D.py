from train_curveadj_fuzzynet_3D import CurveAdjFuzzyNet3D
from matplotlib.pyplot import figure


# BORRAR
from mpl_toolkits.mplot3d.axes3d import get_test_data

class PlotCurveAdjFuzzyNet3D(CurveAdjFuzzyNet3D):
    def __init__(
        self,
        population_size: int,
        tournament_size: float,
        n_generations: int,
        range_considered,
        mutation_allowed: bool,
        **kwargs
        ) -> None:
        
        super().__init__(population_size, tournament_size, n_generations, range_considered, mutation_allowed)

        self.fig = figure(**kwargs)

        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 1, 2, projection='3d')

        self.aptitude_x, self.aptitude_y = [], []


    def plot_curves(self, i: int, **kwargs) -> None:
        self.ax1.clear()
        self.ax1.plot(self.actual_values, color='blue')

        func_with_coef = self.function_to_eval(self.func_string, self.top_winners[i])
        est_curve = self.curve_values(func_with_coef)
        
        self.ax1.plot(est_curve, **kwargs)
        self.ax1.set_ylim(top=max(self.actual_values)*1.1)

        self.ax1.set_title("Curva real vs estimada")


    def plot_error(self, i: int) -> None:
        min_error, max_error = self.top_errors[-1], self.top_errors[0]
        top_error = self.top_errors[i]

        self.aptitude_x.append(i)
        self.aptitude_y.append(top_error)

        self.ax2.clear()
        
        error = f'Gen #{str(i+1).zfill(3)} error: {top_error:.2f}'
        self.ax2.set_title(error)
        # self.ax2.set_xlim([0, self.n_gen])
        self.ax2.set_ylim([min_error*0.9, max_error*1.1])

        self.ax2.plot(self.aptitude_x, self.aptitude_y, color='blue')

    
    def plot_3D(self, i: int) -> None:
        X, Y, Z = get_test_data(0.05)
        self.ax3.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
        self.ax3.set_title(i)


    def plot_curveadj(self, i, **kwargs) -> None:
        self.plot_curves(i, **kwargs)
        self.plot_error(i)
        self.plot_3D(i)