from scipy.signal import find_peaks
import numpy as np
from sys import path
path.insert(0, '..')
from graph_functions import *
from utility_functions import read_file

fig, ax = plt.subplots(1)
ax = format_graph(ax)

files = ['Quarter Period', 'Angular Velocity', 'Max Angle']
files = ['Quarter Period']

for filename in files:
    data = read_file('../Output_data/' + filename)

    be = data['be']
    t = data['time']
    algorithm = data['algo']
    change_indexes = shade_background_based_on_algorithm(t, algorithm, plot=False)

    t = t[change_indexes[0]:]
    be = be[change_indexes[0]:]

    t = t[be > 0]
    be = be[be > 0]


    max_indexes = find_peaks(be)[0]
    be = be[max_indexes]
    t = t[max_indexes]


    # filter out any be encoder recording errors
    no_large_change_indexes = np.diff(be) < 0.25
    t = t[:-1][no_large_change_indexes]
    be = be[:-1][no_large_change_indexes]
    plt.plot(t, be, label=filename)

plt.title('Rotational Quarter Period Algorithm')
# plt.title('Comparison of Timing Algorithms')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r'$(^o)$')
# plt.xlim([0, 390])
plt.legend(loc='best')
plt.show()
fig.savefig(
    'Figures/Comparison.eps', format='eps'
)
