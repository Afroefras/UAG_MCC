from train_tsp import TSP

from matplotlib.pyplot import subplots


class PlotTSP(TSP):
    def __init__(
        self,
        cities_coordinates: list,
        population_size: int,
        n_generations: int,
        tournament_size: float,
    ) -> None:
        super().__init__(
            cities_coordinates, population_size, n_generations, tournament_size
        )
        self.set_plot_env()

    def plot_cities(self, **kwargs) -> None:
        self.axes[0].scatter(self.cit_x, self.cit_y, **kwargs)

    def connectpoints(self, point: tuple, **kwargs) -> None:
        x1, x2 = self.cit_x[point[0]], self.cit_x[point[-1]]
        y1, y2 = self.cit_y[point[0]], self.cit_y[point[-1]]
        self.axes[0].plot([x1, x2], [y1, y2], **kwargs)

    def plot_route(self, i: int, **kwargs) -> None:
        self.axes[0].clear()

        self.axes[0].set_title(f"Best route at gen #{i+1}")
        self.plot_cities(**kwargs)

        route = self.result["route"][i]
        for city in route:
            self.connectpoints(city, **kwargs)

    def plot_distance(self, i: int, **kwargs) -> None:
        min_dist, max_dist = (
            self.result["distance"][self.n_gen - 1],
            self.result["distance"][0],
        )
        top_dist = self.result["distance"][i]
        distance = f"Distance: {top_dist:.2f}"

        self.dist_x.append(i)
        self.dist_y.append(top_dist)

        self.axes[1].clear()

        self.axes[1].set_title(distance)
        self.axes[1].set_xlim([0, self.n_gen])
        self.axes[1].set_ylim([min_dist * 0.9, max_dist])

        self.axes[1].plot(self.dist_x, self.dist_y, **kwargs)

    def set_plot_env(self) -> None:
        self.fig, self.axes = subplots(nrows=1, ncols=2)
        self.cit_x, self.cit_y = [*zip(*self.cit_coor)]

        self.dist_x, self.dist_y = [], []

    def plot_tsp(self, i, **kwargs) -> None:
        self.plot_route(i, **kwargs)
        self.plot_distance(i, **kwargs)
