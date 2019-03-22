import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, moving_average
import numpy as np
from scipy.signal import find_peaks
from collections import OrderedDict


offsets_names = np.genfromtxt('offset_data_collection.csv', delimiter=',', skip_header=1, \
    dtype=['f8','S30','S30','S30'])

files_offsets = {}
for row in offsets_names:
    files_offsets[row[0]] = list(row)[1:]
output_data_directory = '../Output_data/'

for offset in files_offsets.keys():
    dictionary_gradient = OrderedDict({})
    for i, filename in enumerate(files_offsets[offset]):
        if filename != '':
            data = read_file(output_data_directory + filename)
            time = data['time']
            be = data['be']
            algorithm = data['algo']

            # only positive big encoder times
            time = time[be > 0]
            be = be[be > 0]

            # find indexes where algorithm changes
            algorithm_change_indexes = np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))

            # only take data after has switched to quarter period
            time = time[algorithm_change_indexes[1]:]
            be = be[algorithm_change_indexes[1]:]

            # find peaks of big encoder
            peak_index = find_peaks(be)[0]
            maximas = be[peak_index]
            max_times = time[peak_index]

            # always ignore first two peaks after switching algorithm
            maximas = maximas[2:]
            max_times = max_times[2:]

            # plt.plot(max_times, maximas, label='Offset: {}s, run {}'.format(offset, i+1))
            gradient = np.diff(maximas)
            angles = maximas[:-1]

            # find gradient at each value and round it to nearest 0.5, then average 
            # all results in that bin
            for value, gradient_ in zip(angles, gradient):
                round_value = round(2* value)/2
                if round_value not in dictionary_gradient.keys():
                    dictionary_gradient[round_value] = []
                dictionary_gradient[round_value].append(gradient_) 
    # only plot after each offset has been completed
    avg_grad = [np.mean(dictionary_gradient[key]) for key in dictionary_gradient.keys()]
    plt.plot(dictionary_gradient.keys(), avg_grad, label='Offset: {}s, run {}'.format(offset, i+1))

plt.legend(loc='best')
plt.show()