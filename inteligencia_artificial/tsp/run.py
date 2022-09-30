from plot import PlotTSP

from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation

# Coordenadas
cities = [
    (1,3), (2,5), (2,7), (4,2), (4,4), 
    (4,7), (4,8), (5,3), (6,1), (6,6), 
    (7,8), (8,2), (8,7), (9,3), (10,7), 
    (11,1), (11,4), (11,6), (12,7), (13,5),
]

print('\nIniciando ...')
# Parámetros
tsp = PlotTSP(
    cities_coordinates=cities,
    population_size=100,
    n_generations=100,
    tournament_size=0.07,
)

# Entrenamiento
print('\nEntrenando ...')
tsp.train(reprod_functions=[
    tsp.inversion_reprod, 
    tsp.castling_reprod,
])

# Gráfica
anim = FuncAnimation(
    tsp.fig, 
    lambda x: tsp.plot_tsp(x, color=(0.1, 0.2, 0.5)),
    frames=tsp.n_gen,
    interval=300,
    repeat=False,
)
show()
