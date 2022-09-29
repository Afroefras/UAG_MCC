from agente_viajero_01train import TrainTSP
from matplotlib.pyplot import subplots

class TSP(TrainTSP):
    def __init__(self, cities_coordinates: list, population_size: int, n_generations: int, tournament_size: float) -> None:
        super().__init__(cities_coordinates, population_size, n_generations, tournament_size)

    def plot_cities(self) -> None:
        self.fig, self.axes = subplots(nrows=1, ncols=2, figsize=(10, 5))

        self.cit_x, self.cit_y = [*zip(*self.cit_coor)]
        self.axes[0].scatter(self.cit_x, self.cit_y)


    def connectpoints(self, point: tuple, line_color: str, n_gen: int) -> None:
        x1, x2 = self.cit_x[point[0]], self.cit_x[point[-1]]
        y1, y2 = self.cit_y[point[0]], self.cit_y[point[-1]]

        self.axes[0].plot([x1, x2],[y1, y2], c=line_color)
        self.axes[0].set_title(f'Best route, gen #{n_gen}')

    
    def plot_route(self, route: list, **kwargs) -> None:
        self.plot_cities()    
        for city in route:
            self.connectpoints(city, **kwargs)


    def plot_distance(self, train_history: list) -> None:
        self.axes[1].set_xlim([0,100])
        self.axes[1].set_ylim([0, train_history[0][-1]*1.1])

        acum_dist = [x[-1] for x in train_history]
        self.axes[1].plot(acum_dist)

        distance = f'Distance: {acum_dist[-1]:.2f}'
        self.axes[1].set_title(distance)

cities = [
    (1,3), (2,5), (2,7), (4,2), (4,4), 
    (4,7), (4,8), (5,3), (6,1), (6,6), 
    (7,8), (8,2), (8,7), (9,3), (10,7), 
    (11,1), (11,4), (11,6), (12,7), (13,5),
]

t = TSP(cities_coordinates=cities, population_size=10, n_generations=10, tournament_size=0.5)
result = t.train(reprod_functions=[t.inversion_reprod])
print(result)