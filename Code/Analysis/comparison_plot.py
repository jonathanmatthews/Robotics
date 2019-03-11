import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy

output_data_directory = '../Output_data/Lab data 08-03/'
files = sorted(os.listdir(output_data_directory))
text = ["{} {}".format(i, file_) for i, file_ in enumerate(files)]
compare = str(
    input(
        'Select all files to compare, seperate by commas: \n{}\n'.format(
            "\n".join(text))))
# print list(compare)
numbers = list(compare.replace(')', '').replace('(', '').split(','))
files_to_compare = [files[int(i)] for i in numbers if int(i) <= len(files)]

fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
ax = format_graph(ax)

for each_file in files_to_compare:
    angles = read_file(output_data_directory + each_file)
    angles = convert_read_numpy(angles)
    time = angles['time'][20:]
    be = angles['be'][20:]
    angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
    true_max = time[angle_max_index][0]
    plt.plot(time-true_max, be, label=each_file)
    #plt.show()

plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
plt.title('Comparison between different recorded motions')
plt.legend(loc='best')
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
# fig.savefig(
    # 'Figures/Comparison.eps', format='eps')
