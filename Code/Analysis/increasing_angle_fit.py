from graph_functions import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from sys import path
path.insert(0, '..')
from utility_functions import read_file, convert_read_numpy, get_latest_file

# access latest file if underneath file name is blanked out
filename, output_data_directory = get_latest_file('Analysis')
angles = read_file(output_data_directory + filename)
angles = convert_read_numpy(angles)

t = angles['time']
be = angles['be']
algo = angles['algo']

fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax = format_graph(ax)

plt.sca(ax)
algorithm_change_indexes = shade_background_based_on_algorithm(t, algo)
plt.plot(t, be, label='Big Encoder Value')

# [-1] will be final finishing change if it interface finishes in line with algorithm, so [-2] will be when increasing
# algorithm starts
max_times, max_angles = times_and_values_maxima(t, be, start_time=t[algorithm_change_indexes[-2]])
pos_angles_indexes = np.where(max_angles > 0)
max_times = max_times[pos_angles_indexes]
max_angles = max_angles[pos_angles_indexes]
plt.scatter(max_times, max_angles)

def linear_fit(t, a, b):
    return a * t + b

# fit to linear fit
popt, pcov = curve_fit(linear_fit, max_times, max_angles)
# convert to standard error
perr = np.sqrt(np.diag(pcov))

# plot line of best fit
fitted_times = np.linspace(min(max_times), max(max_times), 100)
fitted_values = linear_fit(fitted_times, *popt)
plt.plot(fitted_times, fitted_values, label='Fitted Linear Increase')

# text box with parameter outputs
param_names = ['a', 'b']
text_params = [
    r"${}: {:.3f} \pm {:.3f}$".format(
        name, val, err) for (name, val, err) in 
        zip(param_names, popt, perr)]
plt.text(0.95, 0.05, r'$at + b$' + '\n' + "\n".join(text_params), horizontalalignment='right',
         verticalalignment='bottom',
         transform=ax.transAxes, size=17, bbox=dict(facecolor='lightgrey', alpha=0.9))

# Titles etc
plt.title('Linear fit of maximum angles')
plt.xlabel('Time (s)')
plt.ylabel(r"$Angle (^o)$")
plt.legend(loc='best')
plt.xlim(min(t), max(t))
plt.show()
