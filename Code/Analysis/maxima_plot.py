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

for each_file in files_to_compare:
    angles = read_file(each_file)
    time = angles['time']
    be = angles['be']
    algo = angles['algo']
    algo_change_indexes = shade_background_based_on_algorithm(time, algo, plot=False)
    time = time[algo_change_indexes[1]:]
    be = be[algo_change_indexes[1]:]
    new_time = time[be < 30]
    new_be = be[be < 30]


    window_size = 3
    avg_be = np.array(moving_average(new_be, window_size=window_size))
    avg_time = np.array(moving_average(new_time, window_size=window_size))
    angle_max_index = (np.diff(np.sign(np.diff(avg_be))) < 0).nonzero()[0] + 1 + (window_size - 1)/2
    # true_max = time[angle_max_index][0]

    new_time = time[angle_max_index]
    new_be = be[angle_max_index]

    final_time, final_be = new_time, new_be
    final_time, final_be = np.array(final_time), np.array(final_be)
    final_time -= final_time[0]

    # avg_time = time[be >= 0]
    # avg_be = be[be >= 0]
    avg_be = final_be[final_be > 1]
    avg_time = final_time[final_be > 1]
    # avg_be = np.array(moving_average(final_be, window_size=5))
    # avg_time = np.array(moving_average(final_time, window_size=5))
    plt.plot(avg_time, avg_be, label=get_name(each_file)[:-1])

    avg_be = moving_average(avg_be, 25)
    avg_time = moving_average(avg_time, 25)
    gradient = [diff/(avg_time[i+1] - avg_time[i]) for i, diff in enumerate(np.diff(avg_be))]
    plt.plot(avg_be[1:], gradient)

    # values = {}
    # for i, angle in enumerate(avg_be[:-1]):
    #     rounded_angle = round(angle, 1)
    #     if rounded_angle not in values.keys():
    #         values[rounded_angle] = []
    #     values[rounded_angle].append(avg_be[i+1] - avg_be[i])
    # for key in values:
    #     values[key] = np.mean(values[key])

    # plt.scatter(values.keys(), values.values(), label='Rate of change')
    # plt.plot(time, be, label=get_name(each_file))
    # plt.xlim([0, 415])
    #plt.show()

ax.set_facecolor('white')
ax.set_facecolor('#eeeeee')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
# plt.title('Comparison between different recorded motions')
plt.title('Comparison between rotational and parametric pumping')
plt.legend(loc='best')
fig.tight_layout()
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/RotationalVsParametric.eps', format='eps')
fig.savefig(
    'Figures/RotationalVsParametric.png', format='png'
)
