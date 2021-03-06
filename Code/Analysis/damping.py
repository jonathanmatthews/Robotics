"""
This plot calculates the maximum values recorded from the big encoder and calculates the damping coefficient.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from scipy.optimize import curve_fit
from sys import path
path.insert(0, '..')
from utility_functions import read_file, get_latest_file

filename, output_data_directory = get_latest_file('Analysis')
angles = read_file(output_data_directory + filename)
angles = convert_read_numpy(angles)

t = angles['time']
angle = angles['be']

# taking last position in data and assuming it is same throughout, then
# extracting name to put in title
position_name = angles['pos'][-1]

fig, ax = plt.subplots(1, 1)
ax = format_graph(ax)

plt.title(
    'Damping plot for {} position, taken from data in \n{}'.format(
        position_name,
        filename))
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")

plt.plot(t, angle, label='Collected data')

times_max, angles_max = times_and_values_maxima(t, angle)
plt.scatter(times_max, angles_max, color='r', label='Local maxima')

# calculate period of swing
time_between_max = np.sum(np.diff(times_max)) / (len(times_max) - 1)
w_d = 2 * np.pi / time_between_max


def damping_fit(t, a, b):
    # Function that curve_fit will attempt to fit to
    return a * np.exp(-b * t)

# parameters optimum and covariance matrix
popt, pcov = curve_fit(damping_fit, times_max, angles_max, p0=[30, 0.01])
# convert to standard error
perr = np.sqrt(np.diag(pcov))

time = np.linspace(min(times_max), max(times_max), 100)
angle_fitted = damping_fit(time, *popt)

plt.plot(time, angle_fitted, label='Fitted curve')

# calculates omega without damping and damping coefficient given b and w_d,
# maths taken from wikipedia damping_ratio page on underdamped section


def omega_0(b, w_d): return np.sqrt(b**2 + w_d**2)


def zeta(b, w_d): return b / np.sqrt(b**2 + w_d**2)


# turns values into list to be added to plot
text_params = [
    '{:.3f}'.format(
        val) for val in 
        popt]
# adds all parameters to plot in the bottom right hand corner
plt.text(0.95, 0.05, r'$ae^{-bt} + c$' + '\n' + "\n".join(text_params) + "\n" + r"$\zeta: $" + "{:.4f}".format(zeta(popt[1], w_d)) +
         "\n" + r"$\omega_d: $" + "{:.4f}".format(w_d) +
         "\n" + r"$\omega_0: $" + "{:.4f}".format(omega_0(popt[1], w_d)), horizontalalignment='right',
         verticalalignment='bottom',
         transform=ax.transAxes, size=17, bbox=dict(facecolor='lightgrey', alpha=0.9))

plt.legend(loc='best')
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/DampingPlot{}.png'.format(filename.replace(" ", "")), format='png')
