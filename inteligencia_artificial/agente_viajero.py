from random import sample, randint
from pandas import DataFrame, concat

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
        winner = sample_q.iloc[:1,-1:].reset_index()
        return winner


    def n_tournaments(self, tournament_size_q: float) -> list:
        self.winners = DataFrame()
        for _ in range(self.pop_size):
            winner = self.single_tournament(q=tournament_size_q)
            self.winners = concat([self.winners, winner], axis=0)

        self.winners.sort_values('dist', ascending=True, inplace=True)
        top_winner = self.winners.iloc[0,0]
        top_dist = self.winners.iloc[0,-1]

        top_route_cities = self.df.loc[top_winner, :]
        top_route_cities = top_route_cities.iloc[:-1].tolist()
        top_route = [self.cit_dict[x] for x in top_route_cities]

        self.winners.drop('dist', axis=1, inplace=True)
        self.winners.set_index('index', inplace=True)
        self.winners = self.winners.join(self.df.iloc[:, :-1])

        return top_route, top_dist


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

        winners_list = self.winners.values.tolist()
        for to_reprod in winners_list:
            reprod = self.inversion_reprod(to_reprod)
            self.population.append(reprod)

        self.to_dataframe()


    def train(self) -> None:
        self.create_population()
        self.get_all_dist()

        train_history = []
        for _ in range(self.n_gen):
            top_route, top_dist = self.n_tournaments(tournament_size_q=0.2)
            train_history.append((top_route, top_dist))

            self.new_population()
            self.get_all_dist()

        self.result = DataFrame(train_history, columns=['top_route', 'top_dist'])