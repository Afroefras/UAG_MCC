# Entorno ########################################################################
from plot_curveadj_fuzzynet_3D import PlotCurveAdjFuzzyNet3D

from time import sleep
from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation


# Parámetros ######################################################################
ca = PlotCurveAdjFuzzyNet3D(
    population_size=100,
    tournament_size=0.07,
    n_generations=100,
    x_range=[x/4 for x in range(20)],
    y_range=[y/5 for y in range(25)],
    mutation_allowed=True,
    figsize=(11,7),
)

# Variables ########################################################################
func_to_eval = '100*sin("x")*cos("y")'
surface = ca.surface_values(func_to_eval)

# Entrenamiento ###################################################################
ca.train(
    actual_values=surface,
    scale_dict={
        'M': 20,
        'D': 100,
        'P': 1,
        'Q': 1,
        'R': 1,
    },
    stop_at_n_same_error=25,
    mutation_rate=0.19,
    n_mutations=1,
    verbose=True,
)

# Gráfica ##########################################################################
anim = FuncAnimation(
    ca.fig, 
    # lambda x: ca.plot_curveadj(x, c='red', ls='dashed'),
    ca.plot_curveadj,
    frames=ca.n_gen,
    interval=500,
    repeat=False,
)

sleep(3)
show()
