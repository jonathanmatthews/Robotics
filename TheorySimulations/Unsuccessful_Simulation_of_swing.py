import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from operator import add

g = 9.8
l1 = 4
l2 = 2
l4 = 2
l5 = 2
m1 = 5
m2 = 5
m3 = 10
m4 = 10
m5 = 10
A = 0.5*m2+m3+m4+m5
B = 0.25*m2+m3+m4+m5
C = 0.25*m1+m2+m3+m4+m5

# function that returns dz/dt
def model(state,t,ang4,w4,dw4dt,ang5,w5,dw5dt):
    
    ang1 = state[0]
    w1 = state[1]
    ang2 = state[2]
    w2 = state[3]
    
    ang4 = angle4(t, position, tpp, tpeak[-1], tmove, ang4min, ang4max)+ang2
    ang5 = angle5(t, position, tpp, tpeak[-1], tmove, ang5min, ang5max)+ang2
    
    w4 = omega4(t, position, tpp, tpeak[-1], tmove, ang4min, ang4max)
    w5 = omega5(t, position, tpp, tpeak[-1], tmove, ang5min, ang5max)
    
    dw4dt = domega4dt(t, position, tpp, tpeak[-1], tmove, ang4min, ang4max)
    dw5dt = domega5dt(t, position, tpp, tpeak[-1], tmove, ang5min, ang5max)
    
    dw1dt = (1/(1-(A**2*(np.cos(ang2-ang1))**2)/(B*C)))\
    *(1/(C*l1))\
    *(w1*w2*l2*A*np.sin(ang2-ang1)\
    +w1*w4*l4*m4*np.sin(ang4-ang1)\
    +w1*w5*l5*m5*np.sin(ang5-ang1)\
    -g*np.sin(ang1)*C\
    -dw4dt*l4*m4*np.cos(ang4-ang1)\
    -dw5dt*l5*m5*np.cos(ang5-ang1)\
    -(A/B)*np.cos(ang2-ang1)\
    *(w2*w4*l4*m4*np.sin(ang4-ang2)\
    +w2*w5*l5*m5*np.sin(ang5-ang2)\
    -w1*w2*l1*A*np.sin(ang2-ang1)\
    -g*np.sin(ang2)*A\
    -dw4dt*l4*m4*np.cos(ang4-ang2)\
    -dw5dt*l5*m5*np.cos(ang5-ang2)))
    
    dw2dt = (1/(1-(A*(np.cos(ang2-ang1))**2)/C))\
    *(1/(B*l2))\
    *(w2*w4*m4*l4*np.sin(ang4-ang2)\
    +w2*w5*m5*l5*np.sin(ang5-ang2)\
    -w1*w2*l1*A*np.sin(ang2-ang1)\
    -g*np.sin(ang2)*A\
    -dw4dt*l4*m4*np.cos(ang4-ang2)\
    -dw5dt*l5*m5*np.cos(ang5-ang2)\
    -(A*np.cos(ang2-ang1)/C)\
    *(w1*w2*l2*A*np.sin(ang2-ang1)\
    +w1*w4*l4*m4*np.sin(ang4-ang1)\
    +w1*w5*l5*m5*np.sin(ang5-ang1)\
    -g*np.sin(ang1)*C\
    -dw4dt*l4*m4*np.cos(ang4-ang1)\
    -dw5dt*l5*m5*np.cos(ang5-ang1)))
    
    dstate_dt = [w1,dw1dt,w2,dw2dt]
    
    return dstate_dt

position = 0

"""
def angle4(t,position,w1,w1thresh,ang4min,ang4max)
    if position == 0:
        if abs(w1) > w1thresh:
            a4 = ang4min
"""
def angle4(t, position, tpp, tpeak, tmove, ang4min, ang4max):
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            a4 = ang4min
        elif (t-tpeak) < tpp:
            a4 = (ang4max+ang4min)/2 - ((ang4max-ang4min)/2)*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            a4 = ang4max
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            a4 = ang4max
        elif (t-tpeak) < tpp:
            a4 = (ang4max+ang4min)/2 + ((ang4max-ang4min)/2)*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            a4 = ang4min
    return a4
          
def omega4(t, position, tpp, tpeak, tmove, ang4min, ang4max):
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            o4 = 0
        elif angle4(t, position, tpp, tpeak, tmove, ang4min, ang4max) < ang4max:
            o4 = ((ang4max-ang4min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            o4 = 0
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            o4 = 0
        elif angle4(t, position, tpp, tpeak, tmove, ang4min, ang4max) > ang4min:
            o4 = -((ang5max-ang5min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            o4 = 0
    return o4
    """
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return (ang4max/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak)/tmove)
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return -(ang4max/2)*(np.pi/tmove)*np.sin(2*np.pi*(t-tpeak)/tmove)
    """
def domega4dt(t, position, tpp, tpeak, tmove, ang4min, ang4max):
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            do4 = 0
        elif angle4(t, position, tpp, tpeak, tmove, ang4min, ang4max) < ang4max:
            do4 = ((ang4max-ang4min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            do4 = 0
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            do4 = 0
        elif angle4(t, position, tpp, tpeak, tmove, ang4min, ang4max) > ang4min:
            do4 = -((ang4max-ang4min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            do4 = 0
    return do4
    """
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return (ang4max/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak)/tmove)
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            return ang4max
        else:
            return -(ang4max/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak)/tmove)
    """
def angle5(t, position, tpp, tpeak, tmove, ang5min, ang5max):
    if position == 0:
        if (t-tpeak) < (tpp-tmove):
            a5 = ang5min
        elif (t-tpeak) < tpp:
            a5 = (ang5max+ang5min)/2 - ((ang5max-ang5min)/2)*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            a5 = ang5max
    if position == 1:
        if (t-tpeak) < (tpp-tmove):
            a5 = ang5max
        elif (t-tpeak) < tpp:
            a5 = (ang5max+ang5min)/2 + ((ang5max-ang5min)/2)*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            a5 = ang5min
    return a5
    """
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            return ang5min
        else:
            return (ang5max+ang5min)/2 - ((ang5max-ang5min)/2)*np.cos(np.pi*(t-tpeak)/tmove)
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            return ang5max
        else:
            return (ang5max+ang5min)/2 + ((ang5max-ang5min)/2)*np.cos(np.pi*(t-tpeak)/tmove)
    """
def omega5(t, position, tpp, tpeak, tmove, ang5min, ang5max):
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            o5 = 0
        elif (t-tpeak) < tpp:
            o5 = ((ang5max-ang5min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            o5 = 0
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            o5 = 0
        elif (t-tpeak) < tpp:
            o5 = -((ang5max-ang5min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            o5 = 0
    return o5
    """
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return ((ang5max-ang5min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak)/tmove)
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return -((ang5max-ang5min)/2)*(np.pi/tmove)*np.sin(np.pi*(t-tpeak)/tmove)
    """
    
def domega5dt(t, position, tpp, tpeak, tmove, ang5min, ang5max):
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            do5 = 0
        elif angle5(t, position, tpp, tpeak, tmove, ang5min, ang5max) < ang5max:
            do5 = ((ang5max-ang5min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            do5 = 0
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            do5 = 0
        elif angle5(t, position, tpp, tpeak, tmove, ang5min, ang5max) > ang5min:
            do5 = -((ang5max-ang5min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak-(tpp-tmove))/tmove)
        else:
            do5 = 0
    return do5
    """
    if position == 0:
        if (t-tpeak) <= (tpp-tmove):
            return 0
        else:
            return ((ang5max-ang5min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak)/tmove)
    if position == 1:
        if (t-tpeak) <= (tpp-tmove):
            return ang5max
        else:
            return -((ang5max-ang5min)/2)*(np.pi/tmove)**2*np.cos(np.pi*(t-tpeak)/tmove)
    """

# create a time array from 0..100 sampled at 0.05 second steps
dt = 0.05
t = np.arange(0.0, 200, dt)

ang1 = 10
ang2 = 10
w1 = 0
w2 = 0
tmove = 0.5
ang4max = np.pi/2
ang4min = 0
ang5max = 3*np.pi/2
ang5min = np.pi

args = (angle4,omega4,domega4dt,angle5,omega5,domega5dt)

state = np.radians([ang1,w1,ang2,w2])

ang1s = [0,0]
w1s = [0,0]
ang2s = [0,0]
w2s = [0,0]
tpeak = [0]
tpp = 2.55
positions = []
ang4list = []
ang5list = []
w4list = []
w5list = []
dw4dtlist = []
dw5dtlist = []

for i in range(len(t)):
    Z = integrate.odeint(model, state, t[i:i+2], args)
    state = Z[-1,:]
    
    if abs(ang1s[-1]) > abs(state[0]) and abs(ang1s[-1]) > abs(ang1s[-2]):
        if (t[i] - tpeak[-1]) > (tpp-0.5):
            tpeak.append(t[i])
            if position == 0:
                position = 1
            elif position == 1:
                position = 0
    if len(tpeak) >= 2:
        tpp = tpeak[-1]-tpeak[-2]
    ang1s.append(state[0])
    w1s.append(state[1])
    ang2s.append(state[2])
    w2s.append(state[3])
    ang4list.append(angle4(t[i],position,tpp,tpeak[-1],tmove,ang4min,ang4max))
    ang5list.append(angle5(t[i],position,tpp,tpeak[-1],tmove,ang5min,ang5max))
    w4list.append(omega4(t[i],position,tpp,tpeak[-1],tmove,ang4min,ang4max))
    w5list.append(omega5(t[i],position,tpp,tpeak[-1],tmove,ang5min,ang5max))
    dw4dtlist.append(domega4dt(t[i],position,tpp,tpeak[-1],tmove,ang4min,ang4max))
    dw5dtlist.append(domega5dt(t[i],position,tpp,tpeak[-1],tmove,ang5min,ang5max))
    positions.append(position)

del ang1s[0]
del ang1s[0]
del w1s[0]
del w1s[0]
del ang2s[0]
del ang2s[0]
del w2s[0]
del w2s[0]
#print(tpeak)
#Q = integrate.odeint(model, state, t, args)

#print(state)
"""
peaktimes = []
periods = []

for i in range(len(Q[:,0])-2):
    if Q[i,0] < Q[i+1,0] > Q[i+2,0]:
        peaktimes.append(t[i+1])

for i in range(len(peaktimes)-1):
    periods.append(peaktimes[i+1]-peaktimes[i]) 
"""    

#print(len(ang4list))
#print(len(ang2s))

x1 = l1*np.sin(ang1s)
y1 = -l1*np.cos(ang1s)

x2 = l2*np.sin(ang2s) + x1
y2 = -l2*np.cos(ang2s) + y1

x4 = l4*np.sin(list(map(add, ang4list, ang2s)))+x2
y4 = -l4*np.cos(list(map(add, ang4list, ang2s)))+y2

x5 = l5*np.sin(list(map(add, ang5list, ang2s)))+x2
y5 = -l5*np.cos(list(map(add, ang5list, ang2s)))+y2

fig1 = plt.figure(1)
"""
plt.plot(t[0:200],ang4list[0:200])
plt.plot(t[0:200],w4list[0:200])
plt.plot(t[0:200],dw4dtlist[0:200])
"""
plt.plot(t,ang1s)

fig2 = plt.figure(2)
ax = fig2.add_subplot(111, autoscale_on=False, xlim=(-10, 10), ylim=(-10, 10))
ax.grid()

fig3 = plt.figure(3)
plt.plot(t[0:1000],positions[0:1000])
plt.plot(t[0:1000],ang4list[0:1000])

line4, = ax.plot([], [], 'b.-', lw=1)
line5, = ax.plot([], [], 'b.-', lw=1)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line4.set_data([], [])
    line5.set_data([], [])
    time_text.set_text('')
    return line4, line5, time_text

def animate(i):
    thisx4 = [0, x1[i], x2[i], x4[i]]
    thisy4 = [0, y1[i], y2[i], y4[i]]
    thisx5 = [x2[i],x5[i]]
    thisy5 = [y2[i],y5[i]]

    line4.set_data(thisx4, thisy4)
    line5.set_data(thisx5, thisy5)
    time_text.set_text(time_template % (i*dt))
    return line4, line5, time_text

ani = animation.FuncAnimation(fig2, animate, np.arange(1, len(ang1s)),
                              interval=25, blit=True, init_func=init)

#np.savetxt('/Users/harrytucker/Documents/University/Year 4/Group Studies/time.csv', t, delimiter = ',')
#np.savetxt('/Users/harrytucker/Documents/University/Year 4/Group Studies/angle1.csv', ang1s, delimiter = ',')
#np.savetxt('/Users/harrytucker/Documents/University/Year 4/Group Studies/angle2.csv', ang2s, delimiter = ',')
#np.savetxt('/Users/harrytucker/Documents/University/Year 4/Group Studies/angle4.csv', ang4(t), delimiter = ',')
#np.savetxt('/Users/harrytucker/Documents/University/Year 4/Group Studies/angle5.csv', ang5(t), delimiter = ',')

plt.show()

