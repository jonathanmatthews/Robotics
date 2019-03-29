from scipy.signal import find_peaks
import numpy as np
from sys import path
path.insert(0, '..')
from graph_functions import *
from utility_functions import read_file, moving_average
from scipy.optimize import curve_fit

def linear_fit(x, a, b):
    return a * x + b

fig, ax = plt.subplots(1)
ax = format_graph(ax)

files = ['Quarter Period', 'Final Parametric']

for filename in files:
    data = read_file('../Output_data/' + filename)

    if filename == 'Quarter Period':
        label = 'Rotational'
        limit = 15.0
    if filename == 'Final Parametric':
        label = 'Parametric'
        limit = 12.5

    be = data['be']
    t = data['time']
    algorithm = data['algo']
    change_indexes = shade_background_based_on_algorithm(t, algorithm, plot=False)

    t = t[change_indexes[1]:]
    be = be[change_indexes[1]:]

    t = t[be > 0]
    be = be[be > 0]


    max_indexes = find_peaks(be)[0]
    be = be[max_indexes]
    t = t[max_indexes]


    # filter out any be encoder recording errors
    no_large_change_indexes = np.diff(be) < 0.25
    t = t[:-1][no_large_change_indexes]
    be = be[:-1][no_large_change_indexes]

    plt.plot(t, be, label=label)

    avg_be = moving_average(be, 29)
    avg_time = moving_average(t, 29)
    gradient = [diff/(avg_time[i+1] - avg_time[i]) for i, diff in enumerate(np.diff(avg_be))]

    dictionary_gradient = {}
    for value, gradient_ in zip(avg_be[1:], gradient):
        round_value = round(value, 0)
        if round_value not in dictionary_gradient.keys():
            dictionary_gradient[round_value] = []
        dictionary_gradient[round_value].append(gradient_) 
    avg_grad = [np.mean(dictionary_gradient[key])*2.55 for key in dictionary_gradient.keys()]
    # plt.scatter(dictionary_gradient.keys(), avg_grad, label=label, s=20.0)

    avg_grad = np.array(avg_grad)
    x = np.array(dictionary_gradient.keys())

    y = avg_grad[x < limit]
    x = x[x < limit]

    print x, y
    popt, pcov = curve_fit(linear_fit, x, y)
    print 'Popt, pcov', popt, np.sqrt(np.diag(pcov))
    x_fitted = np.linspace(0, limit, 100)
    y_fitted = linear_fit(x_fitted, *popt)
    # plt.plot(x_fitted, y_fitted)

# plt.axvline(8.620, linestyle='--', color='g', label=r'$\theta$' + ': {} '.format(8.620) + r'$(^o)$')
# plt.legend(loc='best')
# plt.title('Rate of increase of angle for\nparametric and rotational')
# plt.xlabel('Angle '+ r'$(^o)$')
# plt.ylabel('Rate of increase of angle\nper period ' + r'$(^o)$')
# plt.show()

# fig.savefig(
#     'Figures/GradientAnalysis.eps', format='eps'
# )
plt.legend(loc='best')
plt.title('Comparison between parametric and rotational motion')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r'$(^o)$')
plt.show()

fig.savefig(
    'Figures/ParametricRotationalComparison.eps', format='eps'
)