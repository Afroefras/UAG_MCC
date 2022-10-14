from math import sin, cos


from re import findall
from numpy import argmin
from random import randint, sample
from string import ascii_uppercase

class CurveAdjust:
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, range_considered) -> None:
        self.pop_size = population_size
        self.n_gen = n_generations
        self.n_players = int(self.pop_size*tournament_size)
        self.func_range = list(range_considered)
        
        self.get_function()
        self.get_coef()
        self.get_actual_values()
        self.actual_curve_values()


    def get_function(self) -> None:
        # self.func_string = input('\nTomando en cuenta las siguientes consideraciones:\n\t- "x" indica el valor del eje x\n\t- Cada coeficiente a buscar debe estar representada por una letra mayúscula entre comillas dobles, ejemplo:\n\t\t"A"*("B"*sin(x/"C") + "D"*cos(x/"E")) + "F"*x - "G"\nIngresa la función a evaluar:\n')
        self.func_string = '"A"*("B"*sin("x"/"C") + "D"*cos("x"/"E")) + "F"*"x" - "G"'


    def get_coef(self) -> None:
        upper_pattern = '|'.join(map(lambda x: f'"{x}"', ascii_uppercase))
        self.all_coef = findall(upper_pattern, self.func_string)
        self.n_chrom = len(self.all_coef)


    def get_actual_values(self) -> None:
        self.actual_values = {}
        for _coef, actual_value in zip(self.all_coef, (8, 25, 4, 45, 10, 17, 35)):
            self.actual_values[_coef.replace('"','')] = actual_value
        # for _coef in self.all_coef:
            # actual_value = input(f'¿Cuál es el valor real de {_coef}? ')
            # self.actual_values[_coef.replace('"','')] = actual_value
        
    
    def function_to_eval(self, values_list: list) -> str:
        to_eval = self.func_string
        for _keym, _value in zip(self.all_coef, values_list):
            to_eval = to_eval.replace(_keym, str(_value))
        return to_eval


    def evaluate_function(self, to_eval: str, x: int) -> float:
        eval_at_x = to_eval.replace('"x"', str(x))
        return eval(eval_at_x)

    
    def curve_values(self, values_list) -> list:
        curve = []
        func_with_coef = self.function_to_eval(values_list)
        for x in self.func_range:
            y = self.evaluate_function(func_with_coef, x)
            curve.append(y)
        return curve


    def actual_curve_values(self) -> None:
        self.actual_curve = self.curve_values(self.actual_values.values())

    
    def create_population(self) -> None:
        self.population = []
        for _ in range(self.pop_size):
            chrom = []
            for _ in range(self.n_chrom):
                chrom.append(randint(1,255))
            self.population.append(chrom)

        self.population_index = list(range(len(self.population)))

    def get_population_curves(self) -> None:
        self.pop_curves = []
        for indiv in self.population:
            self.pop_curves.append(self.curve_values(indiv))

    
    def get_abs_error(self, real_values: list, estimated_values: list) -> float:
        abs_error = 0
        for real, est in zip(real_values, estimated_values):
            abs_error += abs(real-est)
        return abs_error
    

    def all_abs_error(self) -> None:
        self.pop_error = []
        for indiv_curve in self.pop_curves:
            abs_error = self.get_abs_error(self.actual_curve, indiv_curve)
            self.pop_error.append(abs_error)


    def single_tournament(self) -> tuple:
        sample_indexes = sample(self.population_index, self.n_players)
        sample_players = [self.population[x] for x in sample_indexes]
        sample_errors = [self.pop_error[x] for x in sample_indexes]

        min_index = argmin(sample_errors)
        winner = sample_players[min_index]
        winner_error = sample_errors[min_index]
        winner_index = sample_indexes[min_index]

        return winner, winner_error, winner_index


    def n_tournaments(self) -> list:
        winners = []
        _errors = []
        _indexes = []
        for _ in range(self.pop_size):
            winner, _error, _index = self.single_tournament()
            winners.append(winner)
            _errors.append(_error)
            _indexes.append(_index)

        min_index = argmin(_errors)
        top_winner = winners[min_index]
        top_error = _errors[min_index]
        top_index = _indexes[min_index]

        return top_winner, top_error, top_index

    
    def parent_reprod(self, parent_one: list, parent_two: list) -> list:
        cutoff_point = randint(0, 8*self.n_chrom)
        n_alleles = cutoff_point//8

        child_one = parent_one[:n_alleles]
        child_two = parent_two[:n_alleles]

        if cutoff_point % 8!=0:
            pass


    def train(self) -> None:
        self.create_population()
        self.get_population_curves()
        self.all_abs_error()

ca = CurveAdjust(population_size=50, tournament_size=0.1, n_generations=22, range_considered=range(0,100,50))
# print(ca.n_players)
# # print(ca.func_string)
# # print(ca.dict_coef)
# # print(ca.all_coef)
# # print(ca.population)
# # print(ca.actual_curve)

ca.train()
# print(ca.pop_error)
# ca.single_tournament()
# print(ca.n_tournaments())
ca.parent_reprod([53, 37, 255, 24, 52, 95, 243], [107, 127, 145, 1, 20, 152, 32])