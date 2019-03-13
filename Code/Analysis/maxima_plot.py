import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, moving_average

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
    time = angles['time']
    be = angles['be']

    be -= be[0]
    avg_be = np.array(moving_average(be, window_size=9))
    avg_time = np.array(moving_average(time, window_size=9))
    angle_max_index = (np.diff(np.sign(np.diff(avg_be))) < 0).nonzero()[0] + 1
    # true_max = time[angle_max_index][0]
    avg_be = avg_be[angle_max_index]
    avg_time = avg_time[angle_max_index]

    time, be = [], []
    for time_, be_ in zip(avg_time, avg_be):
        if time_ > 200:
            if be_ > 8.4:
                time.append(time_)
                be.append(be_)
        if time_ <= 200:
            time.append(time_)
            be.append(be_)
    time, be = np.array(time), np.array(be)

    avg_time = time[be >= 0]
    avg_be = be[be >= 0]
    avg_be = np.array(moving_average(avg_be, window_size=15))
    avg_time = np.array(moving_average(avg_time, window_size=15))
    plt.plot(avg_time, avg_be, label=get_name(each_file)[:-1])
    # plt.plot(time, be, label=get_name(each_file))
    plt.xlim([0, 415])
    #plt.show()

plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
# plt.title('Comparison between different recorded motions')
plt.title('Comparison between different methods for\ncalculating the best time to kick')
plt.legend(loc='best')
fig.tight_layout()
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/BestTimingIncreasingMethod.eps', format='eps')
fig.savefig(
    'Figures/BestTimingIncreasingMethod.png', format='png'
)
