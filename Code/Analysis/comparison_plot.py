import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file
from scipy.signal import find_peaks

output_data_directory = '../Output_data/'

def get_files(folder):
    files = sorted(os.listdir(folder))
    text = ["{} {}".format(i, file_) for i, file_ in enumerate(files)]
    compare = str(
        input(
            'Select all files to compare, seperate by commas: \n{}\n'.format(
                "\n".join(text))))
    # print list(compare)
    numbers = list(compare.replace(')', '').replace('(', '').split(','))
    responses = [files[int(i)] for i in numbers if int(i) <= len(files)]
    files = []

    for response in responses:
        try:
            open(folder + response).close()
            files.append(folder + response)
        except IOError: # Response is a folder.
            other = get_files(folder + response + "/")
            for i in other:
                files.append(i)
    
    return files


def get_name(location):
    """
    Get the file name from a path, eg: /home/me/file.jpg -> file.jpg
    """
    result = ""
    for i in range(len(location)):
        if location[-i] == "/":
            break

        result = location[-i] + result
    
    return result


files_to_compare = get_files(output_data_directory)


fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
ax = format_graph(ax)
ax.set_facecolor('#eeeeee')

for each_file in files_to_compare:
    angles = read_file(each_file)
    #angles = convert_read_numpy(angles) # Not sure if this should be here, it seems it was removed since my last pull.
    time = angles['time']
    be = angles['be']
    angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1

    be = be[time > 12.06]
    time = time[time > 12.06]

    print each_file
    if each_file == '../Output_data/Decrease Parametric':
        label = 'Parametric Decrease'
        be -= 1.2
    elif each_file == '../Output_data/decreasingdamping':
        label = 'Natural Damping'
    # true_max = time[angle_max_index][5]

    peak_indexes = find_peaks(be)[0]
    be *= 15.0/be[peak_indexes[1]]
    time -= time[peak_indexes[1]]
    plt.plot(time, be, label=label)
    #plt.xlim([0, max(time)])
    #plt.show()

plt.xlim([0, 60])
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
# plt.title('Comparison between different recorded motions')
# plt.title('Comparison between different feedback\nmethods on maintaining amplitude of ' + r"$10^o$")
plt.title('Parametric decrease compared with natural damping')
plt.legend(loc='best')
fig.tight_layout()
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig('Figures/paradecrease.eps', format='eps')
#fig.savefig(
#    'Figures/ParametricRotationalComparison.png', format='png'
#)
