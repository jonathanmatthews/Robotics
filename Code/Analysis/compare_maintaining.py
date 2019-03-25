import matplotlib.pyplot as plt
import numpy as np
from sys import path
path.insert(0, '..')
from utility_functions import get_latest_file, read_file
from graph_functions import *
from scipy.signal import find_peaks

output_data_directory = '../Output_data/'
files = ['Time Feedback', 'Angle Feedback']

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)


for filename in files:
    angles = read_file(output_data_directory + filename)

    # Extract data
    t = angles['time']
    be = angles['be']
    position = angles['pos']
    algorithm = angles['algo']

    be = be[t > 10]
    t = t[t > 10]

    be = abs(be)

    peak_indexes = find_peaks(be)[0]

    be = be[peak_indexes]
    t = t[peak_indexes]

    plt.plot(t, be, label=filename)


plt.title('Comparison Between Different Methods of Maintaining')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r'$(^o)$')
plt.legend(loc='best')
plt.show()

fig.savefig(
    'Figures/MaintainFeedback.eps', format='eps'
)