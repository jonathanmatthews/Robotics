import numpy as np
import os
import matplotlib.pyplot as plt
from graph_format import format_graph
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy, get_latest_file

# access latest file if underneath file name is blanked out
filename, output_data_directory = get_latest_file('Analysis')
angles = read_file(output_data_directory + filename)
angles = convert_read_numpy(angles)

# Extract data
t = angles['time']
be = angles['be']
position = angles['pos']
algorithm = angles['algo']

# find where algorithm changes and difference in indexes between current and next algorithm
algorithm_change_indexes = np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))
algorithm_change_diff = np.diff(algorithm_change_indexes)

position_numbers = {
    'extended': 1,
    'seated': -1,
    1.0: 'extended/\nfolded',
    -1.0: 'seated/\nunfolded',
    'folded': 1.0,
    'unfolded': -1
}

# find positions and points at which they change
position_number = [position_numbers[i] for i in position]
change_point = np.diff(position_number)
index_change = np.nonzero(change_point)

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))

# use this to format graphs, keeps everything looking the same
ax = format_graph(ax)
# this puts a second axis on the RHS of plot so can have named positions there
ax2 = ax.twinx()

# find times that nao changes position
times_change = t[index_change]
# these are the maxima of the graphs, will be used for fitting to look at trend
angle_max_index = (np.diff(np.sign(np.diff(np.abs(be)))) < 0).nonzero()[0] + 1
true_max = t[angle_max_index][-len(times_change):-1]


# editing top left plot
plt.sca(ax2)
# modify ticks to correct names
locs, labels = plt.yticks()
plt.yticks(np.linspace(min(position_number), max(position_number), 3), [position_numbers[min(position_number)], '', position_numbers[max(position_number)]])
# plot named positions
plt.plot(t, position_number, color='r', label='Position of Nao', linewidth=0.5)

plt.sca(ax)
# for each change in algorithm shade background slightly darker
for i, index in enumerate(algorithm_change_indexes[:-1]):
    plt.axvspan(t[index], t[index + algorithm_change_diff[i]], alpha = (i+1) * 0.15, color='grey', label='{}'.format(algorithm[index+1]))
plt.title('Plot of angle, named position, and algorithm type. \n Data taken from {}'.format(filename))
plt.ylabel('Named position')
plt.xlabel('Time (s)')
plt.plot(t, be, label='Big Encoder', color='b')
plt.xlim([0, max(t)])

# make one big legend not two smaller ones
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines2 + lines, labels2 + labels, loc='lower left', framealpha=1.0)
plt.show()
