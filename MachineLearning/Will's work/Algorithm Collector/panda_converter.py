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
import pandas as pd

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

nets = np.array(nets)
net_fits = np.array([net.fitness for net in nets])

net = nets[np.argmax(net_fits)]


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
print("Min Angle: ", min(angles))

df = pd.DataFrame({"Time":times,"Angles":angles})
df.to_csv("Evolution_data.csv",index=False,header=False)
