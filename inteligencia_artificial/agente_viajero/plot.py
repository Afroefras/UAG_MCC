from matplotlib.pyplot import subplots

class PlotAgenteViajero:
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
