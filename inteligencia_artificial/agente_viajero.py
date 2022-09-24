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

        self.df = DataFrame(self.population, columns=[f'city_{x}' for x in self.cit_name])


    def calculate_distance(self, p: tuple, q: tuple) -> float:
        sqt_diff = 0
        for x, y in zip(p, q):
            sqt_diff += (x - y)**2
        dist = sqt_diff**0.5
        return dist

    
    def aptitude_func(self, chromosone: list) -> None:
        coord = [self.cit_dict[x] for x in chromosone]
        len_coord = len(coord)

        aptitude_result = 0
        for i in range(len_coord - 1):
            aptitude_result += self.calculate_distance(coord[i], coord[i+1])

        return aptitude_result


    def get_all_dist(self) -> list:
        all_dist = []
        for chromosone in self.population:
            aptitude_result = self.aptitude_func(chromosone)
            all_dist.append(aptitude_result)
        
        self.df['dist'] = all_dist


    def single_tournament(self, q: float) -> DataFrame:
        sample_q = self.df.sample(frac=q).copy()
        sample_q.sort_values(by='dist', ascending=False, inplace=True)
        winner = sample_q.iloc[:1,-1:].reset_index()
        return winner


    def n_tournaments(self, tournament_size_q: float) -> DataFrame:
        self.winners = DataFrame()
        for _ in range(self.pop_size):
            winner = self.single_tournament(q=tournament_size_q)
            self.winners = concat([self.winners, winner], axis=0)


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


    def new_population(self) -> None:
        pass

cities = [
    (1,3), (2,5), (2,7), (4,2), (4,4), 
    # (4,7), (4,8), (5,3), (6,1), (6,6), 
    # (7,8), (8,2), (8,7), (9,3), (10,7), 
    # (11,1), (11,4), (11,6), (12,7), (13,5),
]

av = AgenteViajero(cities, population_size=10, n_generations=2)
av.create_population()
# av.get_all_dist()
# av.n_tournaments(tournament_size_q=0.5)

# print('\nPopulation: ', av.population)
# print('\nDistances: ', av.df)
# print('\nPopulation: ', av.df.shape, av.df)
print(av.population[0],'\n\n',av.inversion_reprod(av.population[0]))