"""
===========================
The double pendulum problem
===========================

This animation illustrates the double pendulum problem.
"""

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


L1 = 0.6  # length of pendulum 1 in m
L2 = 0.2  # length of pendulum 2 in m
L3 = 0.1  # length of pendulum 3 in m



angle1 = np.array(10*(list(np.linspace(-np.pi/4,np.pi/4,21))[0:-1]+list(np.linspace(np.pi/4,-np.pi/4,21))[0:-1]))
angle2 = np.array(20*(list(np.linspace(-np.pi/4,np.pi/4,11))[0:-1]+list(np.linspace(np.pi/4,-np.pi/4,11))[0:-1]))
angle3 = np.array(40*(list(np.linspace(-np.pi/4,np.pi/4,6))[0:-1]+list(np.linspace(np.pi/4,-np.pi/4,6))[0:-1]))


# create a time array from 0..100 sampled at 0.05 second steps
dt = 0.05
t = np.arange(0.0, 20, dt)

# th1 and th2 are the initial angles (degrees)
# w10 and w20 are the initial angular velocities (degrees per second)
th1 = 120.0
w1 = 0.0
th2 = -10.0
w2 = 0.0

# initial state


# integrate your ODE using scipy.integrate.


x1 = L1*sin(angle1)
y1 = -L1*cos(angle1)

x2 = L2*sin(angle2) + x1
y2 = -L2*cos(angle2) + y1

x3 = L2*sin(angle3) + x2
y3 = -L2*cos(angle3) + y2



fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-1, 1), ylim=(-1, 0))
ax.grid()

line1, = ax.plot([], [], 'o-', lw=2)
line2, = ax.plot([], [], 'x-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line1.set_data([], [])
    time_text.set_text('')
    return line1, time_text


def animate(i):
    thisx1 = [0, x1[i], x2[i],x3[i]]
    thisy1 = [0, y1[i], y2[i],y3[i]]
    thisx2 = [0, x3[i], x2[i],x1[i]]
    thisy2 = [0, y3[i], y2[i],y1[i]]

    line1.set_data(thisx1, thisy1)
    line2.set_data(thisx2, thisy2)
    

    time_text.set_text(time_template % (i*dt))
    return line1,line2, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(t)),
                              interval=50, blit=True, init_func=init)


# ani.save('double_pendulum.mp4', fps=15)
plt.show()