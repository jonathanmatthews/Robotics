from utility_functions import read_file, convert_read_numpy
"""
This plot shows the angle against time, along with the position of the robot against time.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""

import numpy as np
from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from graph_format import format_graph
from scipy.optimize import curve_fit
from sys import path
path.insert(0, '..')

# access latest file if underneath file name is blanked out
output_data_directory = '../Output_data/'
files = sorted(os.listdir(output_data_directory))
filename = files[-1]
# filename =
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

# finds indexes corresponding to local maxima
# angle_max_index = argrelextrema(angle, np.greater)
t = t[20:]
angle = angle[20:]
angle_max_index = (np.diff(np.sign(np.diff(angle))) < 0).nonzero()[0] + 1
# extracts value corresponding to those indexes
time_max = t[angle_max_index]
angle_max = angle[angle_max_index]
plt.scatter(time_max, angle_max, color='r', label='Local maxima')

# calculate period of swing
time_between_max = np.sum(np.diff(time_max)) / (len(time_max) - 1)
w_d = 2 * np.pi / time_between_max


def damping_fit(t, a, b):
    # Function that curve_fit will attempt to fit to
    return a * np.exp(-b * t)


# parameters optimum and covariance matrix
popt, pcov = curve_fit(damping_fit, time_max, angle_max)
# convert to standard error
perr = np.sqrt(np.diag(pcov))
# create time list and calculate corresponding angles
time = np.linspace(min(time_max), max(time_max), 100)
angle_fitted = damping_fit(time, *popt)

plt.plot(time, angle_fitted, label='Fitted curve')

# calculates omega without damping and damping coefficient given b and w_d,
# maths taken from wikipedia damping_ratio page on underdamped section


def omega_0(b, w_d): return np.sqrt(b**2 + w_d**2)


def zeta(b, w_d): return b / np.sqrt(b**2 + w_d**2)


# turns values into list to be added to plot
text_params = [
    '{:.3f}'.format(
        val[0]) +
    r'$ \pm$' +
    ' {:.3f}'.format(
        val[1]) for val in zip(
        popt,
        perr)]
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
