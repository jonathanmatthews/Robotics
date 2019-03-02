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

position_numbers = {
    'extended': 1,
    'seated': -1,
    1.0: 'extended',
    -1.0: 'seated',
    'folded': 1.0,
    'unfolded': -1
}
position_number = [position_numbers[i] for i in position]
change_point = np.diff(position_number)
index_change = np.nonzero(change_point)

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))

# use this to format graphs, keeps everything looking the same
ax = format_graph(ax)
ax2 = ax.twinx()

times_change = t[index_change]
angle_max_index = (np.diff(np.sign(np.diff(np.abs(be)))) < 0).nonzero()[0] + 1
true_max = t[angle_max_index][-len(times_change):-1]
# editing top left plot
plt.sca(ax2)
locs, labels = plt.yticks()
plt.yticks(np.linspace(min(position_number), max(position_number), 3), [position_numbers[min(position_number)], '', position_numbers[max(position_number)]])
plt.plot(t, position_number, color='r', label='Position of Nao')
plt.sca(ax)
plt.title('Plot of angle and seat position')
plt.ylabel('Named position')
plt.xlabel('Time (s)')
plt.plot(t, be, label='Big Encoder')
plt.show()
