from math import sin, cos


from re import findall
from random import randint
from string import ascii_uppercase

class CurveAdjust:
    def __init__(self, population_size: int, range_considered) -> None:
        self.pop_size = population_size
        self.func_range = range_considered
        
        self.get_function()
        self.get_variables()
        self.get_actual_values()
        self.create_population()


    def get_function(self) -> None:
        # self.func_string = input('\nTomando en cuenta las siguientes consideraciones:\n\t- "x" indica el valor del eje x\n\t- Cada variable a buscar debe estar representada por una letra mayúscula entre comillas dobles, ejemplo:\n\t\t"A"*("B"*sin(x/"C") + "D"*cos(x/"E")) + "F"*x - "G"\nIngresa la función a evaluar:\n')
        self.func_string = '"A"*("B"*sin("x"/"C") + "D"*cos("x"/"E")) + "F"*"x" - "G"'


    def get_variables(self) -> None:
        upper_pattern = '|'.join(map(lambda x: f'"{x}"', ascii_uppercase))
        found_vars = findall(upper_pattern, self.func_string)

        self.all_vars = [x.replace('"','') for x in found_vars]
        self.n_chrom = len(self.all_vars)

        self.dict_vars = {x:i for i,x in enumerate(found_vars)}


    def get_actual_values(self) -> None:
        self.all_values = {}
        for _var, actual_value in zip(self.all_vars, (8, 25, 4, 45, 10, 17, 35)):
            self.all_values[_var] = actual_value
        # for _var in self.all_vars:
            # actual_value = input(f'¿Cuál es el valor real de {_var}? ')
            # self.all_values[_var] = actual_value
        
    
    def evaluate_function(self, chrom: list, x: int) -> float:
        to_eval = self.func_string
        for _keym, _value in self.dict_vars.items():
            to_eval = to_eval.replace(_keym, f'chrom[{_value}]')

        to_eval = to_eval.replace('"x"', str(x))
        return eval(to_eval)


    def create_population(self) -> None:
        self.population = []
        for _ in range(self.pop_size):
            chrom = []
            for _ in range(self.n_chrom):
                chrom.append(randint(1,255))
            self.population.append(chrom)





ca = CurveAdjust(population_size=10, range_considered=range(100))
# print(ca.func_string)
# print(ca.dict_vars)
# print(ca.population)
print(ca.evaluate_function((8, 25, 4, 45, 10, 17, 35), 60))