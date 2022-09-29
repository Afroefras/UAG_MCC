from train import TSP

from matplotlib.pyplot import subplots, show
from matplotlib.animation import ArtistAnimation



class PlotTSP(TSP):
    def __init__(self, cities_coordinates: list, population_size: int, n_generations: int, tournament_size: float) -> None:
        super().__init__(cities_coordinates, population_size, n_generations, tournament_size)

        self.train(reprod_functions=[self.inversion_reprod, self.castling_reprod])

        self.fig, self.axes = subplots(nrows=1, ncols=2)
        self.cit_x, self.cit_y = [*zip(*self.cit_coor)]
        self.axes[1].set_xlim([0, self.n_gen])


    def plot_cities(self, **kwargs) -> None:
        self.axes[0].scatter(self.cit_x, self.cit_y, **kwargs)
        

    def connectpoints(self, point: tuple, **kwargs) -> None:
        x1, x2 = self.cit_x[point[0]], self.cit_x[point[-1]]
        y1, y2 = self.cit_y[point[0]], self.cit_y[point[-1]]
        self.axes[0].plot([x1, x2],[y1, y2], **kwargs)


    def plot_route(self, route: list, n_gen: int, **kwargs) -> None:
        for city in route:
            self.connectpoints(city, **kwargs)
        self.axes[0].set_title(f'Best route, gen #{n_gen}')


    def plot_distance(self, distance_history: list) -> None:
        self.axes[1].plot(distance_history)

        top_dist = list(distance_history)[-1]
        distance = f'Distance: {top_dist:.2f}'
        self.axes[1].set_title(distance)


    def plot_tsp(self, i, **kwargs) -> None:
        self.plot_cities(c='red')
        self.plot_route(route=self.result['route'][i], n_gen=i+1, **kwargs)
        self.plot_distance(distance_history=self.result['distance'][:i+1])


cities = [
    (1,3), (2,5), (2,7), (4,2), (4,4), 
    (4,7), (4,8), (5,3), (6,1), (6,6), 
    (7,8), (8,2), (8,7), (9,3), (10,7), 
    (11,1), (11,4), (11,6), (12,7), (13,5),
]

tsp = PlotTSP(cities_coordinates=cities, population_size=10, n_generations=10, tournament_size=0.5)

ims = []
for i in range(tsp.n_gen):
    ims.append((tsp.plot_tsp(i, c='blue'),))

im_ani = ArtistAnimation(tsp.fig, ims, interval=50, repeat_delay=3000, blit=True)
show()