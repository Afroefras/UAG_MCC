from os import system
from numpy import argmin
from re import findall, sub
from math import exp, sin, cos
from random import randint, sample, choices


class CurveAdjFuzzyNet:
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, range_considered, mutation_allowed: bool) -> None:
        self.n_gen = n_generations
        self.pop_size = population_size
        self.mutation = mutation_allowed
        self.func_range = list(range_considered)
        self.n_players = int(self.pop_size*tournament_size)


    def set_fuzzynet(self) -> None:
        self.func_string = '''
        (
            exp((-("x" - "A")**2) / (2*"D"**2 + 1e-10))*("G"*"x" + "J") + 
            exp((-("x" - "B")**2) / (2*"E"**2 + 1e-10))*("H"*"x" + "K") + 
            exp((-("x" - "C")**2) / (2*"F"**2 + 1e-10))*("I"*"x" + "L")
        ) / (
            exp((-("x" - "A")**2) / (2*"D"**2 + 1e-10)) + 
            exp((-("x" - "B")**2) / (2*"E"**2 + 1e-10)) + 
            exp((-("x" - "C")**2) / (2*"F"**2 + 1e-10)) + 
            + 1e-10
        )
        '''
        self.func_string = sub('\s', '', self.func_string)

    def get_coef(self) -> None:
        self.all_coef = findall('\"[A-Z]\"', self.func_string)
        self.all_coef = sorted(list(set(self.all_coef)))
        self.n_chrom = len(self.all_coef)
        
    
    def function_to_eval(self, _func, values_list: list) -> str:
        to_eval = _func
        for _keym, _value in zip(self.all_coef, values_list):
            to_eval = to_eval.replace(_keym, str(_value))
        return to_eval


    def evaluate_function(self, to_eval: str, x: int) -> float:
        eval_at_x = to_eval.replace('"x"', str(x))
        return eval(eval_at_x)

    
    def curve_values(self, func_with_coef) -> list:
        curve = []
        for x in self.func_range:
            y = self.evaluate_function(func_with_coef, x)
            curve.append(y)
        return curve

    
    def create_population(self) -> None:
        self.population = []
        self.population_index = list(range(self.pop_size))

        for _ in self.population_index:
            chrom = []
            for _ in range(self.n_chrom):
                chrom.append(randint(0, 255) // 10)
            self.population.append(chrom)

        # self.scale_list_of_lists()
        self.get_population_curves()
        self.all_abs_error()

    
    # def scale_list_of_lists(self) -> None:
    #     aux = map(lambda x: [y//self.aux_weight for y in x], self.population) 
    #     self.population = list(aux)


    def get_population_curves(self) -> None:
        self.pop_curves = []
        for indiv in self.population:
            self.pop_curves.append(
                self.curve_values(
                    self.function_to_eval(
                        self.func_string,
                        values_list=indiv
                    )
                )
            )

    
    def get_abs_error(self, real_values: list, estimated_values: list) -> float:
        abs_error = 0
        for real, est in zip(real_values, estimated_values):
            abs_error += abs(real - est)
        return abs_error
    

    def all_abs_error(self) -> None:
        self.pop_error = []
        for indiv_curve in self.pop_curves:
            indiv_error = self.get_abs_error(self.actual_values, indiv_curve)
            self.pop_error.append(indiv_error)


    def single_tournament(self) -> tuple:
        sample_indexes = sample(self.population_index, self.n_players)

        players = [self.population[x] for x in sample_indexes]
        players_error = [self.pop_error[x] for x in sample_indexes]
        players_index = [self.population_index[x] for x in sample_indexes]
        
        min_index = argmin(players_error)
        winner = players[min_index]
        winner_error = players_error[min_index]
        winner_index = players_index[min_index]

        return winner, winner_error, winner_index


    def n_tournaments(self) -> list:
        self.winners = []
        _errors = []
        n_wins = {x:0 for x in self.population_index}

        for _ in range(self.pop_size):
            winner, _error, _index = self.single_tournament()

            while n_wins[_index] >= 3:
                winner, _error, _index = self.single_tournament()        

            n_wins[_index] += 1               
            self.winners.append(winner)
            _errors.append(_error)

        min_index = argmin(_errors)
        top_winner = self.winners[min_index]
        top_error = _errors[min_index]

        return top_winner, top_error

    
    def parents_reprod(self, parent_one: list, parent_two: list) -> tuple:
        cutoff_point = randint(1, 8*self.n_chrom)
        n_gens = cutoff_point // 8
        byte_mod = cutoff_point % 8

        child_one = parent_one[:n_gens]
        child_two = parent_two[:n_gens]

        if byte_mod != 0:
            to_split_one = parent_one[n_gens]
            to_split_two = parent_two[n_gens]

            mask_lower = (2**(8 - byte_mod)) - 1
            mask_upper = 255 - mask_lower

            upper_one = to_split_one & mask_upper
            lower_two = to_split_two & mask_lower
            to_append_one = upper_one | lower_two

            upper_two = to_split_two & mask_upper
            lower_one = to_split_one & mask_lower
            to_append_two = upper_two | lower_one

            child_one.append(to_append_one)
            child_two.append(to_append_two)

            n_gens += 1

        child_one += parent_two[n_gens:]
        child_two += parent_one[n_gens:]

        return child_one, child_two


    def mutate(self, to_mutate: int, n_th: int) -> int:
        mutant = to_mutate ^ (1 << (n_th - 1))
        return mutant


    def mutate_chromosome(self, chromosome: list, n_to_mutate: int, n_mutations: int) -> list:
        mutants_indexes = choices(range(len(chromosome)), k=n_to_mutate)
        for mutant_index in mutants_indexes:
            already_pos = set()
            for _ in range(n_mutations):
                mutation_pos = randint(1,8)
                while mutation_pos in already_pos:
                    mutation_pos = randint(1,8)
                    already_pos.add(mutation_pos)
                
                chromosome[mutant_index] = self.mutate(chromosome[mutant_index], mutation_pos)
        return chromosome


    def mutate_population(self, mutation_rate: float, **kwargs) -> None:
        n_to_mutate = int(self.pop_size*mutation_rate)

        chroms_indexes = sample(self.population_index, n_to_mutate)
        for chrom_index in chroms_indexes:
            chromosome = self.population[chrom_index]
            mutant_chrom = self.mutate_chromosome(chromosome, n_to_mutate, **kwargs)
            self.population[chrom_index] = mutant_chrom


    def new_population(self, **kwargs) -> None:
        self.population = []
        for _ in range(self.pop_size//2):
            parent_one, parent_two = sample(self.winners, 2)
            child_one, child_two = self.parents_reprod(parent_one, parent_two)
            self.population.extend([child_one, child_two])
        
        if self.mutate: self.mutate_population(**kwargs)

        self.get_population_curves()
        self.all_abs_error()


    def train(self, actual_values, stop_at_n_same_error: int, verbose: bool=False, **kwargs) -> None:
        self.actual_values = actual_values

        self.set_fuzzynet()
        self.get_coef()

        func_to_print = self.func_string.replace('"','')
        self.create_population()

        self.top_winners = []
        self.top_errors = []
        for i in range(self.n_gen):
            _winner, _error = self.n_tournaments()
            self.top_winners.append(_winner)
            self.top_errors.append(_error)

            if verbose: 
                system('clear')
                print(f'{func_to_print}\n\nGeneración #{i+1} con {len(self.population)} indiv:\nCoeficientes ganadores {_winner} con error {_error:0.2f}')

            last_n_errors = set(self.top_errors[-stop_at_n_same_error:])
            if i > stop_at_n_same_error and len(last_n_errors) == 1:
                print(f'\nEl error {_error:0.2f} se ha mantenido durante {stop_at_n_same_error} generaciones.\nEntrenamiento terminado :)')
                self.n_gen = i
                break

            self.new_population(**kwargs)
