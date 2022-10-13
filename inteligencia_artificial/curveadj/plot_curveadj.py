from math import sin, cos
from matplotlib.pyplot import subplots, show

class PlotTSP:
    def __init__(self) -> None:
        self.set_plot_env()


    def set_plot_env(self) -> None:
        self.fig, self.axes = subplots(nrows=1, ncols=2, figsize=(10,5))
        self.dist_x, self.dist_y = [], []


    def plot_curve(self, func_to_plot, range_to_plot, **kwargs) -> None:
        self.axes[0].plot([func_to_plot(x) for x in range_to_plot], **kwargs)
        

    def connectpoints(self, point: tuple, **kwargs) -> None:
        x1, x2 = self.cit_x[point[0]], self.cit_x[point[-1]]
        y1, y2 = self.cit_y[point[0]], self.cit_y[point[-1]]
        self.axes[0].plot([x1, x2],[y1, y2], **kwargs)        


    def plot_route(self, i: int, **kwargs) -> None:
        self.axes[0].clear()

        self.axes[0].set_title(f'Best route at gen #{i+1}')
        self.plot_cities(**kwargs)

        route = self.result['route'][i]
        for city in route:
            self.connectpoints(city, **kwargs)


    def plot_distance(self, i: int, **kwargs) -> None:
        min_dist, max_dist = self.result['distance'][self.n_gen-1], self.result['distance'][0]
        top_dist = self.result['distance'][i]
        distance = f'Distance: {top_dist:.2f}'

        self.dist_x.append(i)
        self.dist_y.append(top_dist)

        self.axes[1].clear()

        self.axes[1].set_title(distance)
        self.axes[1].set_xlim([0, self.n_gen])
        self.axes[1].set_ylim([min_dist*0.9, max_dist])

        self.axes[1].plot(self.dist_x, self.dist_y, **kwargs)


    def plot_tsp(self, i, **kwargs) -> None:
        self.plot_route(i, **kwargs)
        self.plot_distance(i, **kwargs)


A, B, C, D, E, F, G = 8, 25, 4, 45, 10, 17, 35

def actual_curve(x) -> float:
    return A*(B*sin(x/C) + D*cos(x/E)) + F*x - G

tsp = PlotTSP()
tsp.plot_curve(actual_curve, range(100), c='r', ls='dashed')
show()