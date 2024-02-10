# Entorno ########################################################################
from plot_curveadj_fuzzynet import PlotCurveAdjFuzzyNet

from time import sleep
from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation


# Parámetros ######################################################################
ca = PlotCurveAdjFuzzyNet(
    population_size=300,
    tournament_size=0.07,
    n_generations=200,
    range_considered=range(100),
    mutation_allowed=True,
    figsize=(11, 7),
)

# Variables ########################################################################
func_to_eval = '8*(25*sin("x"/4)+45*cos("x"/10))+17*"x"-35'
quasipol = ca.curve_values(func_to_eval)

# Entrenamiento ###################################################################
ca.train(
    actual_values=quasipol,
    stop_at_n_same_error=30,
    mutation_rate=0.19,
    n_mutations=1,
    verbose=True,
)

# Gráfica ##########################################################################
anim = FuncAnimation(
    ca.fig,
    lambda x: ca.plot_curveadj(x, c="red", ls="dashed"),
    frames=ca.n_gen,
    interval=200,
    repeat=False,
)

sleep(3)
show()
