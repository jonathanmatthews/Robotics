# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

@author: William
"""
import numpy as np
import settings
import pickle
import pygame
import os
import matplotlib.pyplot as plt

import Seated_Swinging_ML_Will as SSwingEnv

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

env = SSwingEnv.initialise()
observation,env = SSwingEnv.stepper(*env, 0)
r = 0
times = [0]
angles = [observation[0]]
for t in range(30000):
    output = net.output(observation)
    action = output.index(max(output))
    observation,env = SSwingEnv.stepper(*env, action)
    times.append(t/50)
    angles.append(observation[0])
    reward = abs(observation[0])
    r += reward

plt.plot()
plt.plot(times, angles)
plt.xlim(0, max(times))
plt.xlabel("Time/s")
plt.ylabel("Angle/rad")
plt.legend()
plt.show()
