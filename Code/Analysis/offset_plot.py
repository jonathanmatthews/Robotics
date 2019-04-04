import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, moving_average, flatten
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from collections import OrderedDict


offsets_names = np.genfromtxt('offset_data_collection.csv', delimiter=',', skip_header=1, \
    dtype=['f8','S30','S30','S30'])

files_offsets = {}
for row in offsets_names:
    if row[0] != -0.1 and row[0] <= 0.05:
        files_offsets[row[0]] = list(row)[1:]
output_data_directory = '../Output_data/'

def linear_fit(x, m, c, d):
    return m * x + c + d * x ** 2

def exp_fit(x, m, b, c, d):
    return m/b * (1 - np.exp(- b * (x-c))) + d


# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)


information = OrderedDict({})

for offset in sorted(files_offsets.keys()):
    print 'Offset: {:.2f}'.format(offset)
    information[offset] = {
        'gradients': [],
        'periods': [],
    }

    for i, filename in enumerate(files_offsets[offset]):
        if filename != '':
            data = read_file(output_data_directory + filename)
            time = data['time']
            be = data['be']
            algorithm = data['algo']

            for pos in range(2):
                # find indexes where algorithm changes
                algorithm_change_indexes = np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))

                # only take data after has switched to quarter period
                time = time[algorithm_change_indexes[1]:]
                be = be[algorithm_change_indexes[1]:]
                window = 21

                be = np.array(moving_average(be, window_size=window))
                time = time[(window-1)/2:-(window-1)/2]

                if pos == 1:
                    # only positive big encoder times
                    time = time[be > 0]
                    be = be[be > 0]
                if pos == 0:
                    time = time[be < 0]
                    be = be[be < 0]
                    be = np.abs(be)

                # find peaks of big encoder
                peak_index = find_peaks(be)[0]
                maximas = be[peak_index]
                max_times = time[peak_index]

                # always ignore first two peaks after switching algorithm
                maximas = maximas[2:]
                max_times = max_times[2:]

                # filter out any be encoder recording errors
                no_large_change_indexes = np.diff(maximas) < 0.25
                max_times = max_times[:-1][no_large_change_indexes]
                maximas = maximas[:-1][no_large_change_indexes]

                # plt.plot(max_times, maximas, label=offset)

                # curve fit doesn't work with different data types
                max_times = max_times.astype(dtype=np.float32)
                maximas = maximas.astype(dtype=np.float32)
                errors = np.array([0.08]*len(maximas))
                errors = errors.astype(dtype=np.float32)

                periods = np.diff(max_times)
                information[offset]['periods'] = list(information[offset]['periods']) + list(periods)

                popt, pcov = curve_fit(exp_fit, max_times, maximas, p0=[0.08, 0.01, 10.0, 4.5], sigma=errors)
                print 'b: {}, m: {}'.format(popt[1], popt[0])

                fitted_times = np.linspace(min(max_times), max(max_times), 50)
                # fitted_maximas = linear_fit(fitted_times, *popt)
                fitted_maximas = exp_fit(fitted_times, *popt)
                # plt.plot(fitted_times, fitted_maximas, label='Fit')
                # plt.legend(loc='best')
                # plt.show()
                perr = np.sqrt(np.diag(pcov))

                information[offset]['gradients'].append(popt[0])



average_gradients = [np.mean(information[key]['gradients']) for key in information.keys()]
std_gradients = [np.std(information[key]['gradients']) for key in information.keys()]
average_periods = [np.mean(information[key]['periods']) for key in information.keys()]
std_periods = [np.std(information[key]['periods']) for key in information.keys()]
increase_per_cycle = [grad * period for grad, period in zip(average_gradients, average_periods)]
std_increase_per_cycle = [np.sqrt((dg/p)**2 + (-g*dp/p**2)**2) for g, p, dg, dp in zip(average_gradients, average_periods, std_gradients, std_periods)]

plt.errorbar(information.keys(), increase_per_cycle, yerr=std_increase_per_cycle, label='Increase per period', fmt='o')
plt.xlabel('Offset (s)')
plt.ylabel('Increase per period ' + r'$(^o)$')
plt.title('Comparison between different offsets\nand the rate of increase of angle')

# def resonance_curve(x, a, b, c):
#     return 1/((x-a)**2 + (b/2)**2) + c


# resonance_offsets = np.array(information.keys()).astype(dtype=np.float32)
# resonance_values = np.array(increase_per_cycle).astype(dtype=np.float32)
# popt, pcov = curve_fit(resonance_curve, information.keys(), increase_per_cycle, p0=[-0.25, 1.7, -1.1], bounds=([-0.3, -10.0, -1.5], [-0.2, 10, 0.7]))
# perr = np.sqrt(np.diag(pcov))

# print popt

# fitted_times = np.linspace(min(information.keys()), max(information.keys()), 100)
# fitted_values = resonance_curve(fitted_times, *popt)
# plt.plot(fitted_times, fitted_values, label='Resonance fit')

plt.legend(loc='best')
plt.show()