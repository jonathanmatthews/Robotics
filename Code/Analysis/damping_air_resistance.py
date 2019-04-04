from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from graph_functions import *

p = 1.225
c_d = 1.05
g = 9.81
l = 1.8
m = 5.0

def pend(y, t, m, g, l):
    theta, omega = y
    dydt = [omega, - 1.0/(2.0*m) * 1.225 * 0.5 * 1.05 * omega ** 2 * l ** 2 - g/l * np.sin(theta)]
    return dydt



y0 = [20.0, 0.0]
y0 = [y * np.pi/180.0 for y in y0]
print(y0)
t = np.linspace(0, 100, 10001)

sol = odeint(pend, y0, t, args=(m, g, l))

plt.plot(t, sol[:, 0] * 180.0/np.pi, 'b', label='theta(t)')
plt.xlabel('t')
plt.grid()
# plt.show()

# output_data = '../Output_data/'
# filenames = ['Box Masses', 'Box No Masses']

# def damping_fit(t, a, b):
#     return a * np.exp(-b * t)

# for filename in filenames:
#     data = read_file(output_data + filename)

#     t = data['time']
#     be = data['be']

#     max_indexes = find_peaks(be)[0]
#     be = be[max_indexes]
#     t = t[max_indexes]

#     # plt.plot(t, be, label=filename)

#     popt, pcov = curve_fit(damping_fit, t, be)

#     x_fitted = np.linspace(0, 100, 1000)
#     y_fitted = damping_fit(x_fitted, *popt)
#     plt.plot(x_fitted, y_fitted, label='Fitted Damping')

#     angles = np.linspace(2, 20, 50)
#     if filename == 'Box Masses':
#         mass = 6.0
#         energy_lost_per_cycle_masses = [np.abs(np.cos(angle * np.pi/180) - np.cos(damping_fit(2.55, angle, popt[1])*np.pi/180)) * mass for angle in angles]
#     if filename == 'Box No Masses':
#         mass = 1.0
#         energy_lost_per_cycle_no_masses = [np.abs(np.cos(angle * np.pi/180) - np.cos(damping_fit(2.55, angle, popt[1])*np.pi/180)) * mass for angle in angles]
plt.show()


# ratio = [a/b for a,b in zip(energy_lost_per_cycle_masses, energy_lost_per_cycle_no_masses)]
# print ratio
# plt.plot(angles, ratio, label='Energy lost per cycle, file: {}'.format(filename))
# plt.legend(loc='best')
# plt.show()

