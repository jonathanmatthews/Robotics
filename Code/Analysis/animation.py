"""
This code animates the motion recorded by running the interface.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""


from numpy import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from graph_format import format_graph
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy, get_latest_file

L1 = 1.5  # length of pendulum 1 in m
L2 = 0.12  # length of pendulum 2 in m
L3 = 0.20  # length of pendulum 3 in m

filename, output_data_directory = get_latest_file('Analysis')
angles = read_file(output_data_directory + filename)
angles = convert_read_numpy(angles)

# Extract data
angle1 = angles['be']
angle1 = angle1 * pi / 180
angle2 = angles['se0']
angle2 = angle2 * pi / 180
angle3 = angles['se1']
angle3 = angle3 * pi / 180
t = angles['time']
dt = t[-1] - t[-2]
cmx = angles['cmx']
cmy = angles['cmy']

# Convert angles to cartesian coordinates
x1 = L1 * sin(angle1)
y1 = -L1 * cos(angle1)

x2 = L2 * sin(angle1 + angle2) + x1
y2 = -L2 * cos(angle1 + angle2) + y1

x3 = L2 * sin(angle1 + angle2 + angle3) + x2
y3 = -L2 * cos(angle1 + angle2 + angle3) + y2

# Add figure
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False,
                     xlim=(-1.5, 1.5), ylim=(-2.5, 0.5))
ax = format_graph(ax)
ax.grid()
plt.sca(ax)

# Setup lines for later
line1, = ax.plot([], [], 'o-', lw=2, color='b')
line2, = ax.plot([], [], 'o-', lw=2, color='r')
line3, = ax.plot([], [], 'o-', lw=2, color='g')
line4, = ax.plot([], [], 'o-', lw=4, color='y')
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, size=14)


def init():
    # Start up functions, gives clean start
    line1.set_data([], [])
    time_text.set_text('')
    return line1, time_text


def animate(i):
    # Coordinates of masses per frame
    origin = [0, 0]
    m1 = [x1[i], y1[i]]
    m2 = [x2[i], y2[i]]
    m3 = [x3[i], y3[i]]
    cm = [cmx[i], cmy[i]]
    # First list is x-coords of one line, second list is y-coords of same line
    line1.set_data([origin[0], m1[0]], [origin[1], m1[1]])
    line2.set_data([m1[0], m2[0]], [m1[1], m2[1]])
    line3.set_data([m2[0], m3[0]], [m2[1], m3[1]])
    line4.set_data([m3[0], cm[0]], [m3[1], cm[1]])

    time_text.set_text(time_template % t[i])
    return line1, line2, line3, time_text


ani = animation.FuncAnimation(fig, animate, np.arange(0, len(t)),
                              interval=100 * dt/0.1, blit=True, init_func=init)
plt.xlabel('x coordinate')
plt.ylabel('y coordinate')
plt.title('Recorded motion of pendulum \nTaken from file {}'.format(filename))
plt.ylim([-3, 0])
plt.xlim([-1.5, 1.5])


# ani.save('Figures/double_pendulum.mp4', fps=15)
plt.show()
