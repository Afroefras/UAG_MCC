# Entorno ########################################################################

from plot_curveadj import PlotCurveAdj

from time import sleep
from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation


# Función para ajustar y valores reales ###########################################

FUNCTION_TO_ADJUST = '"A"*("B"*sin("x"/("C"+1e-10)) + "D"*cos("x"/("E"+1e-10))) + "F"*"x" - "G"'
ACTUAL_VALUES = (8, 25, 4, 45, 10, 17, 35)


# Parámetros ######################################################################

ca = PlotCurveAdj(
    population_size=400,
    tournament_size=0.05,
    n_generations=100,
    range_considered=range(100),
    mutation_allowed=True,
    figsize=(12,5),
)


# Entrenamiento ###################################################################

ca.train(
    stop_at_n_same_error=15,
    mutation_rate=0.15,
    n_mutations=1,
    verbose=True,  
)

# Gráfica ##########################################################################

anim = FuncAnimation(
    ca.fig, 
    lambda x: ca.plot_curveadj(x, c='red', ls='dashed'),
    frames=ca.n_gen,
    interval=200,
    repeat=False,
)

sleep(3)
show()
