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

save_path = os.path.join(os.getcwd(),"SSwingEnv")
if not os.path.exists(save_path):
    os.makedirs(save_path)

oldest_gen = max([int(x.split(" ")[1].strip(".pkljg")) for x in os.listdir(save_path)])
oldest_str = "Generation "+str(oldest_gen)+".pkl"
gen_path = os.path.join(save_path, oldest_str)

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

with open("Sim-data.csv", "r") as file:
    op_times = []
    op_angle = []
    for i,line in enumerate(file):
        if i > 1700:
            t,a,_ = line.split(",")
            op_times.append(float(t)-34)
            op_angle.append(float(a.strip("\n")))

env = SSwingEnv.initialise(True)
observation,env = SSwingEnv.stepper(*env, 0)
r = 0
times = [0]
angles = [observation[0]]
#actions = [0]
for t in range(settings.max_steps_long_run):
    output = net.output(observation)
    action = [output[:2].index(max(output[:2])), output[2:].index(max(output[2:]))]
    observation,env = SSwingEnv.stepper(*env, action)
    times.append(t/50)
    angle = np.rad2deg(observation[0])
    angles.append(angle)
    #actions.append(action*2-1)
    reward = abs(observation[0])
    r += reward

print("Max Angle: ", max(angles))

plt.figure()
plt.plot(op_times, op_angle, "r", label ="Optimum")
plt.plot(times, angles, "b", label="Angle")
#plt.plot(times, actions, label = "Action")
plt.xlim(0, max(times))
plt.xlabel("Time/s")
plt.ylabel("Angle/deg")
#plt.title("Swing Amplitude over time for generation {}".format(oldest_gen))
plt.legend()
plt.show()
