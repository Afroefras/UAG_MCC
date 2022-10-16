from re import findall
from numpy import argmin
from math import sin, cos
from string import ascii_uppercase
from random import randint, sample

class CurveAdjust:
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, range_considered) -> None:
        self.n_gen = n_generations
        self.pop_size = population_size
        self.func_range = list(range_considered)
        self.n_players = int(self.pop_size*tournament_size)
        
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
        self.population_index = list(range(self.pop_size))

        for _ in self.population_index:
            chrom = []
            for _ in range(self.n_chrom):
                chrom.append(randint(1,255))
            self.population.append(chrom)

        self.get_population_curves()
        self.all_abs_error()


    def get_population_curves(self) -> None:
        self.pop_curves = []
        for indiv in self.population:
            self.pop_curves.append(self.curve_values(indiv))

    
    def get_abs_error(self, real_values: list, estimated_values: list) -> float:
        abs_error = 0
        for real, est in zip(real_values, estimated_values):
            abs_error += abs(real - est)
        return abs_error
    

    def all_abs_error(self) -> None:
        self.pop_error = []
        for indiv_curve in self.pop_curves:
            indiv_error = self.get_abs_error(self.actual_curve, indiv_curve)
            self.pop_error.append(indiv_error)


    def single_tournament(self) -> tuple:
        sample_indexes = sample(self.population_index, self.n_players)

        sample_players = [self.population[x] for x in sample_indexes]
        sample_errors = [self.pop_error[x] for x in sample_indexes]
        
        min_index = argmin(sample_errors)
        winner = sample_players[min_index]
        winner_error = sample_errors[min_index]

        return winner, winner_error


    def n_tournaments(self) -> list:
        self.winners = []
        _errors = []
        for _ in range(self.pop_size):
            winner, _error = self.single_tournament()
            self.winners.append(winner)
            _errors.append(_error)
        min_index = argmin(_errors)
        top_winner = self.winners[min_index]
        top_error = _errors[min_index]

        return top_winner, top_error

    
    def parents_reprod(self, parent_one: list, parent_two: list) -> tuple:
        cutoff_point = randint(0, 8*self.n_chrom)
        n_alleles = cutoff_point // 8
        split_allele = cutoff_point % 8

        child_one = parent_one[:n_alleles]
        child_two = parent_two[:n_alleles]

        complete_allele = 0

        if split_allele != 0:
            to_split_one = parent_one[n_alleles]
            to_split_two = parent_two[n_alleles]

            mask_one = (2**split_allele) - 1
            mask_two = 255 - mask_one

            upper_one = to_split_one & mask_one
            upper_two = to_split_two & mask_one
            lower_one = to_split_one & mask_two
            lower_two = to_split_two & mask_two
            child_one.append(lower_one | upper_two)
            child_two.append(lower_two | upper_one)

            complete_allele = 1

        child_one += parent_two[n_alleles + complete_allele:]
        child_two += parent_one[n_alleles + complete_allele:]

        return child_one, child_two


    def sort_list_based_on_another(self, based_on: list, to_sort: list, top_n: int=None) -> tuple:
        zipped_lists = zip(based_on, to_sort)
        sorted_pairs = sorted(zipped_lists)
        _, result = [list(x) for x in  zip(*sorted_pairs)]
        if top_n is not None:
            return result[:top_n]
        return result


    def new_population(self) -> None:
        self.population = []
        for _ in range(self.pop_size//2):
            parent_one, parent_two = sample(self.winners, 2)
            child_one, child_two = self.parents_reprod(parent_one, parent_two)
            self.population.extend([child_one, child_two])
        
        self.get_population_curves()
        self.all_abs_error()


    def train(self) -> None:
        self.create_population()

        self.train_history = []
        for _ in range(self.n_gen):
            _winner, _error = self.n_tournaments()
            self.train_history.append((_winner, _error))
            self.new_population()
