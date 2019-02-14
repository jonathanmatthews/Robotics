"""
===========================
The double pendulum problem
===========================

This animation illustrates the double pendulum problem.

This code should be run from inside the Analysis directory, otherwise the imports will NOT work.
"""


from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

L1 = 1.5  # length of pendulum 1 in m
L2 = 0.12  # length of pendulum 2 in m
L3 = 0.20 # length of pendulum 3 in m

angles = np.loadtxt('../Output_data/14-02-2019 17:31:40')

angle1 = angles[:, 11]
angle1 = angle1 * np.pi/180.0
print len(angle1)
print angle1
angle2 = angles[:, 7]
angle2 = angle2 * np.pi/180.0
print angle2
angle3 = angles[:, 8]
angle3 = angle3 * np.pi/180.0
print angle3
t = angles[:, 0]
dt = 0.1

x1 = L1*sin(angle1)
y1 = -L1*cos(angle1)

x2 = L2*sin(angle1 + angle2) + x1
y2 = -L2*cos(angle1 + angle2) + y1

x3 = L2*sin(angle1 + angle2 + angle3) + x2
y3 = -L2*cos(angle1+ angle2 + angle3) + y2

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 1), ylim=(-1, 0))
ax.grid()

line1, = ax.plot([], [], 'o-', lw=2)
line2, = ax.plot([], [], 'x-', lw=2)
line3, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line1.set_data([], [])
    time_text.set_text('')
    return line1, time_text


def animate(i):
    origin = [0, 0]
    m1 = [x1[i], y1[i]]
    m2 = [x2[i], y2[i]]
    m3 = [x3[i], y3[i]]

    line1.set_data([origin[0], m1[0]], [origin[1], m1[1]])
    line2.set_data([m1[0], m2[0]], [m1[1], m2[1]])
    line3.set_data([m2[0], m3[0]], [m2[1], m3[1]])

    time_text.set_text(time_template % (i*dt))
    return line1, line2, line3, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                              interval=100, blit=True, init_func=init)
plt.ylim([-4, 0])
plt.xlim([-2, 2])

# ani.save('double_pendulum.mp4', fps=15)
plt.show()
