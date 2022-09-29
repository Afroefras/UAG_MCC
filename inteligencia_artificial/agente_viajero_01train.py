from pandas import DataFrame, concat
from random import sample, randint, choice

class TrainTSP:
    def __init__(self, cities_coordinates: list, population_size: int, n_generations: int, tournament_size: float) -> None:
        self.n_gen = n_generations
        self.pop_size = population_size
        self.tournament_size = tournament_size

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


    def n_tournaments(self) -> list:
        self.winners = DataFrame()
        for _ in range(self.pop_size):
            winner = self.single_tournament(q=self.tournament_size)
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

        first_point = randint(0, len(parent) - 1)
        end_point = randint(first_point + 1, len(parent))

        fragment = parent[first_point:end_point]
        inversion = fragment[::-1]

        child = parent[:first_point] + inversion + parent[end_point:]

        if to_keep==0: return prev_winner[:1] + child
        else: return child + prev_winner[-1:]


    def castling_reprod(self, parent: list) -> list:
        if randint(1,10)==1: return parent

        first_point = randint(0, len(parent) - 2)

        max_len_to_switch = len(parent[first_point:]) // 2
        len_to_switch = randint(1, max_len_to_switch)        

        first_point_end = first_point + len_to_switch

        end_point = randint(first_point_end, len(parent) - len_to_switch)
        end_point_end = end_point + len_to_switch

        child = parent[:first_point] 
        child += parent[end_point:end_point_end]
        child += parent[first_point_end:end_point]
        child += parent[first_point:first_point_end]
        child += parent[end_point_end:]
        return child


    def new_population(self, reprod_func) -> None:
        self.population = []

        just_cities = self.winners.iloc[:, 1:].copy()
        winners_list = just_cities.values.tolist()
        for to_reprod in winners_list:
            reprod = reprod_func(to_reprod)
            self.population.append(reprod)

        self.to_dataframe()
        self.get_all_dist()


    def create_route(self, cities: list) -> None:
        return [(cities[i], cities[i+1]) for i in range(len(cities)-1)]


    def train(self, reprod_functions: list) -> None:
        self.create_population()

        train_history = []
        for _ in range(self.n_gen):
            top_cities, top_dist = self.n_tournaments()

            top_route = self.create_route(top_cities)
            train_history.append((top_cities, top_route, top_dist))
        
            reprod_func = choice(reprod_functions)
            self.new_population(reprod_func=reprod_func)

        return DataFrame(train_history, columns=['cities', 'route', 'distance'])
