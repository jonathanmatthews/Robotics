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

import Seated_Stiff_with_body as SSwingEnv

gen_path = os.path.join("nets_full_move.pkl")

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


env = SSwingEnv.initialise(False)
observation,env,body_angle,leg_angle = SSwingEnv.stepper(*env, 0)
r = 0
times = [0]
angles = [observation[0]]
body_angles = [body_angle]
leg_angles = [leg_angle]
for t in range(settings.max_steps_long_run):
    output = net.output(observation)
    action = [output[:2].index(max(output[:2])), output[2:].index(max(output[2:]))]#output.index(max(output))
    observation,env,body_angle,leg_angle = SSwingEnv.stepper(*env, action)
    times.append(t/50)
    angle = np.rad2deg(observation[0])
    angles.append(angle)
    body_angles.append(body_angle)
    leg_angles.append(leg_angle)
    reward = abs(observation[0])
    r += reward

print("Max Angle: ", max(angles))
print("Min Angle: ", min(angles))

df = pd.DataFrame({"Time":times,"Angles":angles,"Body Angles":body_angles,"Leg Angles":leg_angles})
df.to_csv("Evolution_data_with_body.csv",index=False,header=False)
