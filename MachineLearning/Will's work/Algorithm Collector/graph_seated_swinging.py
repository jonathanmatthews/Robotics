# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

Produces energy and angle graphs for the best brain

@author: William
"""
import numpy as np
import settings
import pickle
import os
import matplotlib.pyplot as plt

import Seated_Stiff as SSwingEnv

gen_path = os.path.join("nets.pkl")

nets = []
file = open(gen_path, "rb")
while True:
    try:
        nets.append(pickle.load(file))
    except EOFError:
        break
file.close()
#    if sum_net_fits == 0:
#        probs = None
#    else:
#        probs = [fit/sum_net_fits for fit in  net_fits]
nets = np.array(nets)
net_fits = np.array([net.fitness for net in nets])

net = nets[np.argmax(net_fits)]

with open("Testing_Algorithm_data.csv", "r") as file:
    op_times = []
    op_angle = []
    for line in file:
        t,a = line.split(",")
        op_times.append(float(t))
        op_angle.append(float(a.strip("\n")))

env = SSwingEnv.initialise(False)
observation,env = SSwingEnv.stepper(*env, 0)
r = 0
times = [0]
angles = [observation[0]]
for t in range(settings.max_steps_long_run):
    output = net.output(observation)
    action = output.index(max(output))
    observation,env = SSwingEnv.stepper(*env, action)
    times.append(t/50)
    angle = np.rad2deg(observation[0])
    angles.append(angle)
    reward = abs(observation[0])
    r += reward

print("Max Angle: ", max(angles))

plt.figure()
plt.plot(times, angles, "b", label="Angle")
#plt.plot(times, actions, label = "Action")
#plt.plot(op_times, op_angle, "r", label ="Robotics Team")
plt.xlim(0, max(times))
plt.xlabel("Time/s")
plt.ylabel("Angle/deg")
#plt.title("Swing Amplitude over time for generation {}".format(oldest_gen))
plt.legend()
plt.show()
