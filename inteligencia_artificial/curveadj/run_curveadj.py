# Entorno
from plot_curveadj import PlotCurveAdj

from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation

##############################################################################################

# Función para ajustar y valores reales
FUNCTION_TO_ADJUST = '"A"*("B"*sin("x"/"C") + "D"*cos("x"/"E")) + "F"*"x" - "G"'
ACTUAL_VALUES = (8, 25, 4, 45, 10, 17, 35)

##############################################################################################

# Parámetros
ca = PlotCurveAdj(
    population_size=250, 
    tournament_size=0.05,
    n_generations=30,
    range_considered=range(50)
)

##############################################################################################

# Entrenamiento
ca.train()

##############################################################################################

# Gráfica
anim = FuncAnimation(
    ca.fig, 
    lambda x: ca.plot_curveadj(x, c='red', ls='dashed'),
    frames=ca.n_gen,
    interval=100,
    repeat=False,
)
show()
