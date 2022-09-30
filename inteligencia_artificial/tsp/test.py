from numpy import arange, hypot
from matplotlib.pyplot import Normalize, figure, pcolor, show
from matplotlib.animation import ArtistAnimation

fig2 = figure()

x = arange(-9, 10)
y = arange(-9, 10).reshape(-1, 1)
base = hypot(x, y)
ims = []
for add in arange(15):
    ims.append((pcolor(x, y, base + add, norm=Normalize(0, 30)),))

im_ani = ArtistAnimation(fig2, ims, interval=50, repeat_delay=3000, blit=True)

show()