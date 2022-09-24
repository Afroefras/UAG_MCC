from random import sample, randint
from re import T
from pandas import DataFrame, concat

from matplotlib.pyplot import axes, plot, title, show

from IPython.display import clear_output

class AgenteViajero:
    def __init__(self, cities_coordinates: list, population_size: int, n_generations: int) -> None:
        self.n_gen = n_generations
        self.pop_size = population_size

        self.cit_coor = cities_coordinates
        self.cit_len = len(self.cit_coor)
        self.cit_dict = dict(enumerate(self.cit_coor))
        self.cit_name = list(self.cit_dict.keys())


    def create_population(self) -> None:
        self.population = []
        for _ in range(self.pop_size):
            indiv = sample(self.cit_name, self.cit_len)
            self.population.append(indiv)

        self.to_dataframe()
        self.get_all_dist()


    def to_dataframe(self) -> None:
        self.df = DataFrame(self.population, columns=self.cit_name)


    def calculate_distance(self, p: tuple, q: tuple) -> float:
        sqt_diff = 0
        for x, y in zip(p, q):
            sqt_diff += (x - y)**2
        dist = sqt_diff**0.5
        return dist

    
    def aptitude_func(self, chromosone: list) -> float:
        coord = [self.cit_dict[x] for x in chromosone]
        len_coord = len(coord)

        aptitude_result = 0
        for i in range(len_coord - 1):
            aptitude_result += self.calculate_distance(coord[i], coord[i+1])

        return aptitude_result


    def get_all_dist(self) -> None:
        all_dist = []
        for chromosone in self.population:
            aptitude_result = self.aptitude_func(chromosone)
            all_dist.append(aptitude_result)
        
        self.df['dist'] = all_dist


    def single_tournament(self, q: float) -> DataFrame:
        sample_q = self.df.sample(frac=q).copy()
        sample_q.sort_values(by='dist', ascending=True, inplace=True)
        winner = sample_q.iloc[:1,:].reset_index()
        return winner


    def n_tournaments(self, tournament_size_q: float) -> list:
        self.winners = DataFrame()
        for _ in range(self.pop_size):
            winner = self.single_tournament(q=tournament_size_q)
            self.winners = concat([self.winners, winner], axis=0)

        self.winners.sort_values('dist', ascending=True, inplace=True)
        top_winner = self.winners.iloc[0,0]
        top_dist = self.winners.iloc[0,-1]

        top_cities = self.df.loc[top_winner, :]
        top_cities = top_cities.iloc[:-1].tolist()
        top_cities = [int(x) for x in top_cities]

        self.winners.drop('dist', axis=1, inplace=True)

        return top_cities, top_dist


    def inversion_reprod(self, prev_winner: list) -> list:
        to_keep = randint(0,1)
        if to_keep==0: parent = prev_winner[1:]
        else: parent = prev_winner[:-1]

        first_point = randint(0, len(parent) - 2)
        end_point = randint(first_point + 2, len(parent))

        fragment = parent[first_point:end_point]
        inversion = fragment[::-1]

        child = parent[:first_point] + inversion + parent[end_point:]

        if to_keep==0: return prev_winner[:1] + child
        else: return child + prev_winner[-1:]


    def new_population(self) -> None:
        self.population = []

        just_cities = self.winners.iloc[:, 1:].copy()
        winners_list = just_cities.values.tolist()
        for to_reprod in winners_list:
            reprod = self.inversion_reprod(to_reprod)
            self.population.append(reprod)

        self.to_dataframe()
        self.get_all_dist()


    def plot_cities(self) -> None:
        self.cit_x, self.cit_y = [*zip(*self.cit_coor)]
        self.ax_cities = axes()
        self.ax_cities.scatter(self.cit_x, self.cit_y)


    def connectpoints(self, point: tuple, line_color: str) -> None:
        x1, x2 = self.cit_x[point[0]], self.cit_x[point[-1]]
        y1, y2 = self.cit_y[point[0]], self.cit_y[point[-1]]
        plot([x1, x2],[y1, y2], c=line_color)

    
    def plot_route(self, route: list, distance: float, line_color: str) -> None:
        self.plot_cities()
        
        distance = f'Distance: {distance:.2f}'
        title(distance)
        for city in route:
            self.connectpoints(city, line_color=line_color)
        show()


    def train(self) -> None:
        self.create_population()

        train_history = []
        for _ in range(self.n_gen):
            top_cities, top_dist = self.n_tournaments(tournament_size_q=0.2)
            top_route = [(top_cities[i], top_cities[i+1]) for i in range(len(top_cities)-1)]
            train_history.append((top_cities, top_route, top_dist))
            
            clear_output(wait=True)
            self.plot_route(route=top_route, distance=top_dist, line_color='blue') 

            self.new_population()

        self.result = DataFrame(train_history, columns=['top_cities', 'top_route', 'top_dist'])