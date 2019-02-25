import numpy as np
import os
import matplotlib.pyplot as plt
from graph_format import format_graph
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy

output_data_directory = '../Output_data/'
files = os.listdir(output_data_directory)
text = ["{} {}".format(i, file_) for i, file_ in enumerate(files)]
compare = str(
    input(
        'Select all files to compare, seperate by commas: \n{}\n'.format(
            "\n".join(text))))
# print list(compare)
numbers = list(compare.replace(')', '').replace('(', '').replace(',', ''))[0::2]
files_to_compare = [files[int(i)] for i in numbers]

fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
ax = format_graph(ax)

for each_file in files_to_compare:
    angles = read_file(output_data_directory + each_file)
    angles = convert_read_numpy(angles)
    plt.plot(angles['time'], angles['be'], label=each_file)

plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
plt.title('Comparison between different recorded motions')
plt.legend(loc='best')
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/Comparison.eps', format='eps')