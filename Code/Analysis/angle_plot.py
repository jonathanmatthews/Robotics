"""
This plot shows the angle against time, along with the position of the robot against time.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""

import numpy as np
from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from graph_format import format_graph


# access latest file if underneath file name is blanked out
files = os.listdir('Output_data/')
files.sort()
filename = files[-1]
# filename = '15-02-2019 10:29:57'
angles = loadtxt('Output_data/' + filename)

position_names = {
    1: 'extended',
    0: 'seated',
    -1: 'initial_seated'
}

# Extract data
t = angles[:, 0]
accx = angles[:, 1]
accy = angles[:, 2]
accz = angles[:, 3]
gx = angles[:, 4]
gy = angles[:, 5]
gz = angles[:, 6]
angle1 = angles[:, 11]
position = angles[:, -1]

# setup figure
fig, ax = plt.subplots(
    2, 2, figsize=(
        8, 6), gridspec_kw={
            'height_ratios': [
                1, 1]}, sharex=True)

# use this to format graphs, keeps everything looking the same
ax = format_graph(ax)

# editing top left plot
plt.sca(ax[0])
plt.title('Plot of angle against seat position')
plt.plot(t, position, label='Position of Nao')
plt.yticks([-1, 0, 1], ['initial_seated', 'seated', 'extended'])
plt.ylabel('Named position')
plt.ylim([min(position)-0.1, max(position)+0.1])

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
fig.savefig('Analysis/Figures/AnglePlot{}.eps'.format(filename.replace(" ", "")), format='eps')
