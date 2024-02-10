# Entorno ########################################################################
from plot_curveadj import PlotCurveAdj

from time import sleep
from matplotlib.pyplot import show
from matplotlib.animation import FuncAnimation

# Parámetros ######################################################################
ca = PlotCurveAdj(
    population_size=400,
    tournament_size=0.05,
    n_generations=100,
    range_considered=range(100),
    mutation_allowed=True,
    figsize=(12, 5),
)

# Entrenamiento ###################################################################
ca.train(
    stop_at_n_same_error=15,
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
