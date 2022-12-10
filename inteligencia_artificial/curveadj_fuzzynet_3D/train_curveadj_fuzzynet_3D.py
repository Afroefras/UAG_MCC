from os import system
from typing import Dict
from numpy import argmin
from math import exp, sin, cos
from string import ascii_uppercase
from re import findall, sub, search
from random import randint, sample, choices



class CurveAdjFuzzyNet3D:
    def __init__(self, population_size: int, tournament_size: float, n_generations: int, x_range, y_range, mutation_allowed: bool) -> None:
        self.n_gen = n_generations
        self.pop_size = population_size
        self.mutation = mutation_allowed

        self.x_range = list(x_range)
        self.y_range = list(y_range)

        self.n_players = int(self.pop_size*tournament_size)


    def set_fuzzynet(self) -> None:
        self.func = {}
        for j in ('M','D'):
            for i in range(6):
                to_add = f'{j}{i+1}'
                self.func[to_add] = f'"{to_add}"'

        for j in ('P','Q','R'):
            for i in range(9):
                to_add = f'{j}{i+1}'
                self.func[to_add] = f'"{to_add}"'

        for i in range(6):
            var = '"x"' if i < 3 else '"y"'
            self.func[f'mf{i+1}'] = f'exp(-({var} - {self.func[f"M{i+1}"]})**2 / 2*{self.func[f"D{i+1}"]}**2)'

        n = 1
        for i in range(3):
            for j in range(3,6):
                self.func[f'inf{n}'] = f"({self.func[f'mf{i+1}']})*({self.func[f'mf{j+1}']})"
                self.func[f'reg{n}'] = f'''
                    {self.func[f'inf{n}']}*({self.func[f"P{n}"]}*"x" + {self.func[f"Q{n}"]}*"y" + {self.func[f"R{n}"]})
                '''
                n += 1

        self.func['a'] = [y for x,y in self.func.items() if search('reg',x) is not None]
        self.func['a'] = ' + '.join(self.func['a'])

        self.func['b'] = [y for x,y in self.func.items() if search('inf',x) is not None]
        self.func['b'] = ' + '.join(self.func['b'])    

        self.func_string = f"({self.func['a']}) / ({self.func['b']})"
        self.func_string = sub('\s', '', self.func_string)


    def get_coef(self) -> None:
        self.all_coef = findall('\"[A-Z]\d\"', self.func_string)
        self.all_coef = sorted(list(set(self.all_coef)))
        self.n_chrom = len(self.all_coef)
        
    
    def function_to_eval(self, _func, values_list: list) -> str:
        to_eval = _func
        for _keym, _value in zip(self.all_coef, values_list):
            to_eval = to_eval.replace(_keym, str(_value))
        return to_eval


    def evaluate_function(self, to_eval: str, x: int, y: int) -> float:
        eval_at_x = to_eval.replace('"x"', str(x))
        eval_at_y = eval_at_x.replace('"y"', str(y))
        try: return eval(eval_at_y)
        except ZeroDivisionError: return 1e10

    
    def surface_values(self, func_with_coef) -> list:
        surface = []
        for x in self.x_range:
            curve = []
            for y in self.y_range:
                y = self.evaluate_function(func_with_coef, x, y)
                curve.append(y)
            surface.append(curve)
        return surface


    def create_scale_dict(self, scale_dict: Dict) -> None:
        pos_dict = {x.replace('"',''): i for i,x in enumerate(self.all_coef)}
        self.scale_dict_pos = {}
        for x,y in pos_dict.items():
            first_letter = x[0]
            self.scale_dict_pos[y] = scale_dict[first_letter]
        print(self.scale_dict_pos)

    
    def scale(self, to_scale: int, scale_dict: Dict, position: int) -> int:
        return to_scale // scale_dict[position]


    def create_population(self) -> None:
        self.population = []
        self.population_index = list(range(self.pop_size))
        
        for _ in self.population_index:
            chrom = []
            for i in range(self.n_chrom):
                to_append = randint(0, 255)
                scaled = self.scale(to_append, self.scale_dict_pos, position=i)
                print(to_append, scaled)
                chrom.append(scaled)
            self.population.append(chrom)

        self.get_population_surfaces()
        self.all_abs_error()


    def get_population_surfaces(self) -> None:
        self.pop_surfaces = []
        for indiv in self.population:
            self.pop_surfaces.append(
                self.surface_values(
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
        for indiv_surface in self.pop_surfaces:
            indiv_error = 0
            for i, indiv_curve in enumerate(indiv_surface):
                to_get_error = self.actual_values[i]
                indiv_error += self.get_abs_error(to_get_error, indiv_curve)
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
        for _ in range(self.pop_size // 2):
            parent_one, parent_two = sample(self.winners, 2)
            child_one, child_two = self.parents_reprod(parent_one, parent_two)
            self.population.extend([child_one, child_two])
        
        if self.mutate: self.mutate_population(**kwargs)

        self.get_population_surfaces()
        self.all_abs_error()


    def train(self, actual_values, scale_dict: Dict, stop_at_n_same_error: int, verbose: bool=False, **kwargs) -> None:
        self.actual_values = actual_values

        self.set_fuzzynet()
        self.get_coef()

        self.create_scale_dict(scale_dict)
        self.create_population()

        self.top_winners = []
        self.top_errors = []
        for i in range(self.n_gen):
            _winner, _error = self.n_tournaments()
            self.top_winners.append(_winner)
            self.top_errors.append(_error)

            if verbose: 
                system('clear')
                print(f'Generación #{i+1} con {len(self.population)} indiv:\nCoeficientes ganadores {_winner} con error {_error:0.2f}')

            last_n_errors = set(self.top_errors[-stop_at_n_same_error:])
            if i > stop_at_n_same_error and len(last_n_errors) == 1:
                print(f'\nEl error {_error:0.2f} se ha mantenido durante {stop_at_n_same_error} generaciones.\nEntrenamiento terminado :)')
                self.n_gen = i
                break

            self.new_population(**kwargs)
