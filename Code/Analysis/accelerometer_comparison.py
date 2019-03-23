import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path, argv
path.insert(0, '..')
from utility_functions import read_file, get_latest_file, total_angle
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset


# access latest file if underneath file name is blanked out
# filename, output_data_directory = get_latest_file('Analysis', test=test)
output_data_directory = '../Output_data/'
files = ['Accelerometer Data No Movement', 'Accelerometer Data']


# setup figure
fig, axis = plt.subplots(
    2, 1, figsize=(
    13, 8), sharex=True)
axis = format_graph(axis)


for i, filename in enumerate(files):
    plt.sca(axis[i])
    angles = read_file(output_data_directory + filename)

    # Extract data
    t = angles['time']
    be = angles['be']
    position = angles['pos']
    algorithm = angles['algo']
    accz = angles['az']
    accz = accz[t > 10]
    t = t[t > 10]
    accz = accz[t < 27.5]
    t = t[t < 27.5]


    if i == 0:
        plt.title('Z Accelerometer Readings for Static Posture')
        # axis[i].set_xticks([])
    if i == 1:
        plt.title('Z Accelerometer Readings for Changing Posture')
    plt.plot(t, accz, label='Z Accelerometer Values', color='r')
    plt.legend(loc='upper left')
plt.xlabel('Time (s)')
fig.text(0.04, 0.5, 'Acceleration' + r'$(ms^{-2})$', va='center', rotation='vertical', size=18)
# fig.tight_layout()
plt.show()
fig.savefig('Figures/AccelerometerComparison.eps', format='eps')
