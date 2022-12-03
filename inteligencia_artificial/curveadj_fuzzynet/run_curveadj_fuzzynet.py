# Entorno ########################################################################
from plot_curveadj_fuzzynet import PlotCurveAdj

from time import sleep
from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation


# Parámetros ######################################################################
ca = PlotCurveAdj(
    population_size=400,
    tournament_size=0.05,
    n_generations=200,
    range_considered=range(100),
    mutation_allowed=True,
    figsize=(12,5),
)

# Variables ########################################################################
func_to_eval = '8*(25*sin("x"/4)+45*cos("x"/10))+17*"x"-35'
quasipol = ca.curve_values(func_to_eval)

# Entrenamiento ###################################################################
ca.train(
    actual_values=quasipol,
    stop_at_n_same_error=100,
    mutation_rate=0.19,
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
