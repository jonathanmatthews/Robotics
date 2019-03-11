from graph_functions import *
import matplotlib.pyplot as plt
import numpy as np
from sys import path
from scipy.optimize import curve_fit
path.insert(0, '..')
from utility_functions import read_file, get_latest_file

def linear_fit(t, a, b):
    return a * t + b

def fit_data(function, t, value):
    # parameters of fit
    popt, pcov = curve_fit(function, t, value)
    # convert covariance matrix into standard error on parameter
    perr = np.sqrt(np.diag(pcov))

    fitted_time = np.linspace(min(t), max(t), 100)
    fitted_value = function(fitted_time, *popt)

    return fitted_time, fitted_value


# access latest file if underneath file name is blanked out
latest_filename, output_data_directory = get_latest_file('Analysis')

# add all files wanting to be compared to the list
files_to_compare = [latest_filename]
fits = ['linear']

fit_dict = {
    'linear': linear_fit
}

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))
ax = format_graph(ax)

for i, _file in enumerate(files_to_compare):
    # collect the data
    angles = read_file(output_data_directory + _file)

    # Extract data
    t = angles['time']
    be = angles['be']
    algorithm = angles['algo']

    # find indexes where the algorithm changes
    algo_change_indexes = algorithm_change_indexes(algorithm)
    # [0] is first algorithm (start), [1] is second (increasing)
    increase_index = algo_change_indexes[1]

    # only take time from switch point, change time relative to this point
    t = t[increase_index:] - t[increase_index]
    # only take encoder values from this point
    be = be[increase_index:]

    # extract all maximas
    time_max, be_max = times_and_values_maxima(t, be)
    # only take maximas that are positive (data has lots of local maxima for negative values)
    pos_angles_indexes = np.where(be_max > 0)
    time_max = time_max[pos_angles_indexes]
    be_max = be_max[pos_angles_indexes]

    # scatter time of maximum and maximum
    plt.scatter(time_max, be_max, label='{}'.format(_file))

    # if there is a function in the list for this value then use it to fit
    if fits[i] in fit_dict.keys():
        # fitted time and values given fit function
        fitted_time, fitted_value = fit_data(fit_dict[fits[i]], time_max, be_max)
        plt.plot(fitted_time, fitted_value)




plt.title('Comparison between different increasing algorithms')
plt.legend(loc='lower right')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
plt.show()

