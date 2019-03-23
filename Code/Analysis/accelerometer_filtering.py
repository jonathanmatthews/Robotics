import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path, argv
path.insert(0, '..')
from utility_functions import read_file, get_latest_file, total_angle
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from scipy.signal import filtfilt, butter

# Filter the data, and plot both the original and filtered signals.
def final_filter(time, values):

    # Filter requirements.
    order = 6
    fs = 1.0/np.mean(np.diff(time[-200:]))
    lowcut = 0.30 # desired cutoff frequency of the filter, Hz
    highcut = 0.50

    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    padded_signal = filtfilt(b, a, values)

    return padded_signal

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


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
    3, 1, figsize=(
        13, 8), sharex=True)

axis = format_graph(axis)

ax0, ax1, ax2 = axis
plt.sca(ax0)
plt.ylabel('Acceleration\n' + r'$(ms^{-2})$')
# adding titles etc, this will add to ax
plt.title('Extraction of Large Encoder Values from Accelerometer Data')

plt.plot(t, accz, label='Original Z Accelerometer Values', color='r')
plt.legend(loc='upper left')
plt.xlim([145, 175])

plt.sca(ax1)
plt.ylabel('Acceleration\nDifference\n' + r'$(ms^{-2})$')

filtered_accz = final_filter(t, accz)
# plt.plot(t, filtered_accz, label='Filtered Z Accelerometer', color='r')
# plt.legend(loc='upper left')
plt.plot(t + 2.55/4.0, -filtered_accz, label='Final Z Accelerometer Values', color='r')
plt.legend(loc='upper left')

plt.sca(ax2)
plt.plot(t, be, label='Large Encoder Values', color='b')
plt.legend(loc='upper left')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r'$(^o)$')
labels = plt.yticks()[0]
labels = [str(label) for label in labels]
labels[1] = ''
ax2.set_yticklabels(labels)

# fig.text(0.01, 0.66, 'Acceleration ' + r'$(ms^{-2})$', va='center', rotation='vertical', size=18)
fig.tight_layout()
plt.show()
fig.savefig(
    'Figures/AccelerometerFiltering.eps', format='eps')