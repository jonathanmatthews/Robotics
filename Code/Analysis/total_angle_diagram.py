import matplotlib.pyplot as plt
import numpy as np
from graph_functions import *
import matplotlib.patches as patches


L1 = 1.5  # length of pendulum 1 in m
L2 = 0.12  # length of pendulum 2 in m
L3 = 0.20  # length of pendulum 3 in m

def create_rods(angles):
    angles_rad = [angle * np.pi/180.0 for angle in angles]
    angle1, angle2, angle3 = angles_rad

    x0, y0 = 0.0, 0.0

    x1 = L1 * abs(np.sin(angle1))
    y1 = -L1 * abs(np.cos(angle1))

    x2 = L2 * abs(np.sin(angle1 + angle2)) + x1
    y2 = -L2 * abs(np.cos(angle1 + angle2)) + y1

    x3 = L3 * abs(np.sin(angle1 + angle2 + angle3)) + x2
    y3 = -L3 * abs(np.cos(angle1 + angle2 + angle3)) + y2

    xs = [x0, x1, x2, x3]
    ys = [y0, y1, y2, y3]

    return xs, ys

def plot_rods(xs, ys):
    colors = ['cornflowerblue', 'forestgreen', 'tomato']
    for i in range(0, len(xs)-1):
        plt.plot(xs[i:i+2], ys[i:i+2], color=colors[i])

fig, ax = plt.subplots(
    1, 1)

ax = format_graph(ax)

ax.set_aspect('equal')

angles = [30.0, 0.0, 0.0]
xs, ys = create_rods(angles)
plot_rods(xs, ys)
plt.plot([xs[0], xs[0]], [ys[0], ys[0]-1.5], color='black', linestyle='--')
plt.scatter(xs, ys, color='black', zorder=100)
plt.text(0.1, 0.5, r'$\theta_b$', horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=28)
plt.xticks([])
plt.yticks([])

style="Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style, color="k")
a3 = patches.FancyArrowPatch((0.0,-1.0), (0.5,-0.86), zorder=90.0, connectionstyle="arc3,rad=.33", **kw)
plt.gca().add_patch(a3)


offset_x = 1.2
angles = [30.0, 40.0, 30.0]
xs, ys = create_rods(angles)
xs = [x + offset_x for x in xs]
plot_rods(xs, ys)
plt.plot([xs[0], xs[0]], [ys[0], ys[0]-1.5], color='black', linestyle='--')
plt.plot([xs[0], xs[-1]], [ys[0], ys[-1]], linestyle='--')
plt.scatter(xs, ys, color='black', zorder=100)
plt.text(0.58, 0.5, r"$\theta_t$", horizontalalignment='center',
     verticalalignment='center',
     transform=ax.transAxes, size=28)
plt.xticks([])
plt.yticks([])

style="Simple,tail_width=0.5,head_width=4,head_length=8"
kw = dict(arrowstyle=style, color="k")
a3 = patches.FancyArrowPatch((0.0+offset_x, -1.0), (0.61+offset_x,-0.79), zorder=90.0, connectionstyle="arc3,rad=.33", **kw)
plt.gca().add_patch(a3)

fig.tight_layout()
plt.show()
fig.savefig('Figures/TotalAngleDiagram.eps', format='eps')

