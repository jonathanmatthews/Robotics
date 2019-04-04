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
filename = 'Accelerometer Algor Tst'
angles = read_file(output_data_directory + filename)

# Extract data
t = angles['time']
be = angles['be']
position = angles['pos']
algorithm = angles['algo']
accz = angles['az']

be = be[t > 145]
accz = accz[t > 145]
algorithm = algorithm[t > 145]
position = position[t > 145]
t = t[t > 145]
be = be[t < 175]
accz = accz[t < 175]
algorithm = algorithm[t < 175]
position = position[t < 175]
t = t[t < 175]


# setup figure
fig, axis = plt.subplots(
    2, 1, figsize=(
        13, 8), sharex=True, gridspec_kw={'height_ratios': [1.5, 1]})

axis = format_graph(axis)

ax, ax1 = axis
plt.sca(ax)

# adding titles etc, this will add to ax
plt.title('Determining when to kick using accelerometer data')
plt.ylabel('Angle ' + r"$(^o)$")

plt.plot(t, be, label='Big Encoder', color='b')
plt.xlim([145, 175])

if True:
    ax2 = ax.twinx()
    ax2 = format_graph(ax2)
    plt.sca(ax2)
    add_named_position_plot(t, position)
    combine_multiple_legends([ax, ax2], custom_location='upper left')
else:
    plt.legend(loc='upper left')


plt.sca(ax1)
plt.plot(t, accz, label='Z Accelerometer Data', color='r')

plt.ylabel('Acceleration ' + r'$(ms^{-2})$')
plt.xlabel('Time (s)')
plt.legend(loc='upper left')
fig.tight_layout()
plt.show()
fig.savefig(
    'Figures/PositionAccelerometer.eps', format='eps')
