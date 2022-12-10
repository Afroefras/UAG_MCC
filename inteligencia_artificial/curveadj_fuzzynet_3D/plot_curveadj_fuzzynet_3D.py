from train_curveadj_fuzzynet_3D import CurveAdjFuzzyNet3D
from matplotlib.pyplot import figure

from scipy.stats import norm
from numpy import array, arange


class PlotCurveAdjFuzzyNet3D(CurveAdjFuzzyNet3D):
    def __init__(
        self, population_size: int,
        tournament_size: float,
        n_generations: int,
        x_range,
        y_range,
        mutation_allowed: bool,
        **kwargs
    ) -> None:
    
        super().__init__(population_size, tournament_size, n_generations, x_range, y_range, mutation_allowed)

        self.fig = figure(**kwargs)

        self.ax1 = self.fig.add_subplot(2, 2, 1, projection='3d')
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 1, 2)

        self.aptitude_x, self.aptitude_y = [], []


    def plot_actual_surface(self, i: int, **kwargs) -> None:
        self.X = array([[x for _ in self.y_range] for x in self.x_range])
        self.Y = array([[y for y in self.y_range] for _ in self.x_range])
        Z = array(self.actual_values)
        self.ax1.plot_surface(self.X, self.Y, Z, **kwargs)

    
    def plot_est_surface(self, i: int, **kwargs) -> None:
        func_with_coef = self.function_to_eval(self.func_string, self.top_winners[i])
        est_surface = self.surface_values(func_with_coef)

        Z = array(est_surface)
        self.ax1.plot_wireframe(self.X, self.Y, Z, **kwargs)
        self.ax1.set_title("Superficie real vs estimada")


    def plot_error(self, i: int) -> None:
        min_error, max_error = self.top_errors[-1], self.top_errors[0]
        top_error = self.top_errors[i]

        self.aptitude_x.append(i)
        self.aptitude_y.append(top_error)

        self.ax2.clear()
        
        error = f'Gen #{str(i+1).zfill(2)} error: {top_error:.2f}'
        self.ax2.set_title(error)
        self.ax2.set_xlim([0, self.n_gen])
        self.ax2.set_ylim([min_error*0.9, max_error*1.1])

        self.ax2.plot(self.aptitude_x, self.aptitude_y, color='blue')


    def plot_gaussians(self, i) -> None:

        self.ax3.clear()

        medians = [self.top_winners[i][self.medians_pos[x]] for x in self.medians_pos]
        std_devs = [self.top_winners[i][self.std_devs_pos[x]] for x in self.std_devs_pos]

        medians_title = ", ".join([f'{x:.0f}' for x in medians])
        std_devs_title = ", ".join([f'{x:.0f}' for x in std_devs])
        self.ax3.set_title(f'Medianas: {medians_title}  -  Desv: {std_devs_title}')

        x_axis = arange(
            min(medians) - 1.5*max(std_devs)**(1/2),
            max(medians) + 1.5*max(std_devs)**(1/2),
            1
        )

        for _median, std_dev in zip(medians, std_devs):
            self.ax3.plot(x_axis, norm.pdf(x_axis, _median, std_dev))


    def plot_curveadj(self, i) -> None:
        self.ax1.clear()
        self.plot_actual_surface(i, color='red')
        self.plot_est_surface(i, color='blue')
        self.plot_error(i)
        self.plot_gaussians(i)
