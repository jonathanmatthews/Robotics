"""
This plot shows the angle against time, along with the position of the robot against time.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""

import numpy as np
from numpy import loadtxt
import os
import matplotlib.pyplot as plt
from graph_format import format_graph
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit


# access latest file if underneath file name is blanked out
files = os.listdir('../Output_data/')
files.sort()
filename = files[-1]
# filename = '15-02-2019 10:29:57'
angles = loadtxt('../Output_data/' + filename)
t = angles[:, 0]
angle = angles[:, 11]

fig, ax = plt.subplots(1, 1)
ax = format_graph(ax)

plt.title('Angle versus time')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$^o$")

plt.plot(t, angle, label='Collected data')

# finds indexes corresponding to local maxima
angle_max_index = argrelextrema(angle, np.greater)
# extracts value corresponding to those indexes
time_max = t[angle_max_index]
angle_max = angle[angle_max_index]
plt.scatter(time_max, angle_max, color='r', label='Local maxima')

def damping_fit(t, a, b, c):
    # Function that curve_fit will attempt to fit to
    return a * np.exp(-b * t) + c

# parameters optimum and covariance matrix
popt, pcov = curve_fit(damping_fit, time_max, angle_max)
# convert to standard error
perr = np.sqrt(np.diag(pcov))
# create time list and calculate corresponding angles
time = np.linspace(min(time_max), max(time_max), 100)
angle_fitted = damping_fit(time, *popt)

plt.plot(time, angle_fitted, label='Fitted curve')

#adds equation to graph
text_params = ['{:.3f}'.format(val[0]) + r'$ \pm$' + ' {:.3f}'.format(val[1]) for val in zip(popt, perr)]
plt.text(0.85, 0.1, r'$ae^{-bt} + c$' +'\n' + "\n".join(text_params), horizontalalignment='right',
     verticalalignment='center',
     transform=ax.transAxes, size=14)

plt.legend(loc='best')
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig('Figures/DampingPlot{}.eps'.format(filename.replace(" ", "")), format='eps')