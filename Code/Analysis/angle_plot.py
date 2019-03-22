"""
This plot shows the angle against time, along with the position of the robot against time, along with gyrometer and accelerometer values.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.



THIS PLOT ISN'T THAT USEFUL NOW
"""

import numpy as np
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, get_latest_file


# access latest file if underneath file name is blanked out
#filename, output_data_directory = get_latest_file('Analysis')
output_data_directory = '../Output_data/'
filename ='22-03-2019 14:23:53 Org'
angles = read_file(output_data_directory + filename)

# Extract data
t = angles['time']
accx = angles['ax']
accy = angles['ay']
accz = angles['az']
gx = angles['gx']
gy = angles['gy']
gz = angles['gz']
angle1 = angles['be']
position = angles['pos']

# setup figure
fig, ax = plt.subplots(
    2, 2, figsize=(
        8, 6), sharex=True)

# use this to format graphs, keeps everything looking the same
ax = format_graph(ax)

# editing top left plot
plt.sca(ax[0])
add_named_position_plot(t, position)
plt.ylabel('Named position')

# editing bottom left plot
plt.sca(ax[2])
plt.plot(t, angle1, label='Big Encoder')
plt.xlabel('Time (s)')
plt.ylabel('Angle (' + r'$^o)$')
plt.grid()

plt.legend(loc='upper left')

# upper right plot
plt.sca(ax[1])
plt.title('Plot of accelerometer values')
plt.plot(t, accx, label='Acceleration x')
plt.plot(t, accy, label='Acceleration y')
plt.plot(t, accz, label='Acceleration z')
plt.legend(loc='lower left')

# lower right plot
plt.sca(ax[3])
plt.title('Plot of gyrometer values')
plt.plot(t, gx, label='Gyro x')
plt.plot(t, gy, label='Gyro y')
plt.plot(t, gz, label='Gyro z')
plt.legend(loc='best')

plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/AnglePlot{}.eps'.format(filename.replace(" ", "")), format='eps')
