"""
This code animates the motion recorded by running the interface.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""


from numpy import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, get_latest_file, cm_to_cartesian

L1 = 1.5  # length of pendulum 1 in m
L2 = 0.12  # length of pendulum 2 in m
L3 = 0.20  # length of pendulum 3 in m

filename, output_data_directory = get_latest_file('Analysis')
filename = '19-03-2019 09:58:47 Org'
angles = read_file(output_data_directory + filename)

# Extract data
angle1 = angles['be']
angle1 = angle1 * pi / 180
angle2 = angles['se0']
angle2 = angle2 * pi / 180
angle3 = angles['se1']
angle3 = angle3 * pi / 180
t = angles['time']
dt = t[-1] - t[-2]
dt = 0.06
cmx = angles['cmx']
cmy = angles['cmy']
algorithm = angles['algo']
print angle2

# Convert angles to cartesian coordinates
x1 = L1 * sin(angle1)
y1 = -L1 * cos(angle1)

x2 = L2 * sin(angle1 + angle2) + x1
y2 = -L2 * cos(angle1 + angle2) + y1

x3 = L3 * sin(angle1 + angle2 + angle3) + x2
y3 = -L3 * cos(angle1 + angle2 + angle3) + y2


# Add figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        15, 15))

ax = format_graph(ax)
ax.grid()
plt.sca(ax)

# Setup lines for later
line1, = ax.plot([], [], 'o-', lw=2, color='b')
line2, = ax.plot([], [], 'o-', lw=2, color='r')
line3, = ax.plot([], [], 'o-', lw=2, color='g')
line4, = ax.plot([], [], 'o-', lw=4, color='y')
line5, = ax.plot([], [], '-', lw=1, linestyle='--', color='b')
line6, = ax.plot([], [], '-', lw=1, linestyle='--', color='b')
line7, = ax.plot([], [], 'o-', lw=1, color='y')

time_template = 'Time: %.1fs'
algorithm_template = 'Algorithm: %s'
max_angle_template = 'Max Angle: %.2f ' + r"$(^o)$"
min_angle_template = 'Min Angle: %.2f ' + r"$(^o)$"
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, size=14)
centre_mass_text = ax.text(0.67, 0.4, 'Centre of mass with respect to seat', transform=ax.transAxes, size=14)
max_angle_text = ax.text(0.05, 0.85, '', transform=ax.transAxes, size=14)
min_angle_text = ax.text(0.05, 0.80, '', transform=ax.transAxes, size=14)
algorithm_text = ax.text(0.05, 0.75, '', transform=ax.transAxes, size=14)
plt.axvspan(-1.5, 1.5, facecolor='grey', alpha=0.15)

max_angle = 0
min_angle = 0
  

def init():
    # Start up functions, gives clean start
    line1.set_data([], [])
    time_text.set_text('')
    return line1, time_text


def animate(i):
    global max_angle, min_angle

    # Coordinates of masses per frame
    origin = [0, 0]
    m1 = [x1[i], y1[i]]
    m2 = [x2[i], y2[i]]
    m3 = [x3[i], y3[i]]
    cm = cm_to_cartesian(angle1[i], angle2[i], angle3[i], [cmx[i], cmy[i]])
    
    enlarged_cm = [5*cmx[i], 5*cmy[i]]
    centre_of_mass_start = [1.0, -1.5]
    centre_of_mass_end = [coord[0] + coord[1] for coord in zip(centre_of_mass_start, enlarged_cm)]


    # First list is x-coords of one line, second list is y-coords of same line
    line1.set_data([origin[0], m1[0]], [origin[1], m1[1]])
    line2.set_data([m1[0], m2[0]], [m1[1], m2[1]])
    line3.set_data([m2[0], m3[0]], [m2[1], m3[1]])
    line4.set_data([m3[0], cm[0]], [m3[1], cm[1]])
    line7.set_data([centre_of_mass_start[0], centre_of_mass_end[0]], [centre_of_mass_start[1], centre_of_mass_end[1]])

    time_text.set_text(time_template % t[i])
    algorithm_text.set_text(algorithm_template % algorithm[i])

    current_angle = np.arctan(x3[i]/y3[i]) * 180/np.pi
    if current_angle > max_angle:
        max_angle = current_angle
        line5.set_data([origin[0], m3[0]], [origin[1], m3[1]])
    if current_angle < min_angle:
        min_angle = current_angle
        line6.set_data([origin[0], m3[0]], [origin[1], m3[1]])

    max_angle_text.set_text(min_angle_template % min_angle)
    min_angle_text.set_text(max_angle_template % max_angle)
    return line1, line2, line3, line4, time_text, algorithm_text, line5, line6, line7, min_angle_text, max_angle_text


ani = animation.FuncAnimation(fig, animate, np.arange(0, len(t)),
                              interval=150 * dt/0.10, blit=True, init_func=init)
plt.xlabel('x coordinate')
plt.ylabel('y coordinate')
plt.title('Recorded motion of pendulum \nTaken from file {}'.format(filename))
plt.ylim([-3, 0])
plt.xlim([-1.5, 1.5])


#ani.save('Figures/double_pendulum.mp4', fps=30)
plt.show()
