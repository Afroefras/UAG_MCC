# Entorno ########################################################################

from plot_curveadj import PlotCurveAdj

from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation


# Función para ajustar y valores reales ###########################################

FUNCTION_TO_ADJUST = '"A"*("B"*sin("x"/"C") + "D"*cos("x"/"E")) + "F"*"x" - "G"'
ACTUAL_VALUES = (8, 25, 4, 45, 10, 17, 35)


# Parámetros ######################################################################

ca = PlotCurveAdj(
    population_size=500, 
    tournament_size=0.05,
    n_generations=100,
    range_considered=range(100),
    mutation_allowed=True,
)


# Entrenamiento ###################################################################

ca.train(
    mutation_rate=0.1,
    n_mutations=1,    
)

# Gráfica ##########################################################################

anim = FuncAnimation(
    ca.fig, 
    lambda x: ca.plot_curveadj(x, c='red', ls='dashed'),
    frames=ca.n_gen,
    interval=10,
    repeat=False,
)
show()