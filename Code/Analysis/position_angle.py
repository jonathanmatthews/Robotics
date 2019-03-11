import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path, argv
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy, get_latest_file

test = False
if argv[-1] == 'Testing':
    test = True
if argv[-1] == 'Real':
    test = False
# access latest file if underneath file name is blanked out
filename, output_data_directory = get_latest_file('Analysis', test=test)
filename = '11-03-2019 10:31:59 Org'
angles = read_file(output_data_directory + filename)
angles = convert_read_numpy(angles)

# Extract data
t = angles['time']
be = angles['be']
position = angles['pos']
algorithm = angles['algo']

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)


# editing plot that will show angle
plt.sca(ax)
shade_background_based_on_algorithm(t, algorithm)

# adding titles etc, this will add to ax
plt.title('Plot of angle, named position, and algorithm being run. \n Data taken from {}'.format(filename))
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")

# plotting angle versus time
plt.plot(t, be, label='Big Encoder', color='b')
plt.xlim([0, max(t)])

# editing axis that will have named positions on
if test:
    # make a copy of axis and overlay it, this way can have angles and named position on same plot
    ax2 = ax.twinx()
    ax2 = format_graph(ax2)
    plt.sca(ax2)
    add_named_position_plot(t, position)
    # make one big legend not two smaller ones
    combine_multiple_legends([ax, ax2], custom_location='lower left')
else:
    plt.legend(loc='best')

fig.tight_layout()
plt.show()
fig.savefig(
    'Figures/SeminarCombined.png', format='png')
