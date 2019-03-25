import matplotlib.pyplot as plt
import numpy as np
from sys import path
path.insert(0, '..')
from utility_functions import get_latest_file, read_file
from graph_functions import *
from scipy.signal import find_peaks

output_data_directory = '../Output_data/'
files = ['Time Feedback', 'Angle Feedback', 'MaintainGoodBad 10 degrees']

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)


for i, filename in enumerate(files):
    angles = read_file(output_data_directory + filename)

    # Extract data
    t = angles['time']
    be = angles['be']
    position = angles['pos']
    algorithm = angles['algo']

    be = be[t > 10]
    t = t[t > 10]

    t = t[be > 0]
    be = be[be > 0]

    be = be[t < 68]
    t = t[t < 68]

    peak_indexes = find_peaks(be)[0]

    be = be[peak_indexes]
    t = t[peak_indexes]

    print i
    if i == 2:
        label = 'Good Bad Kick'
    else:
        label = filename

    plt.plot(t, be, label=label)

plt.xlim([10, 70])
plt.title('Comparison Between Different Methods of\nMaintaining at 10' + r'$^o$')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r'$(^o)$')
plt.legend(loc='lower left')
plt.show()

fig.savefig(
    'Figures/MaintainComparison.eps', format='eps'
)