# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:52:58 2019

@author: William
"""
import settings
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

import Seated_Swinging_no_push_ML_Will as SSwingEnv

save_path = os.path.join(os.getcwd(),"SSwingNoPushEnv")
if not os.path.exists(save_path):
    os.makedirs(save_path)
try:
    gen_lst = [x.split(" ") for x in os.listdir(save_path)]
    gen_lst = [x[1] for x in gen_lst if x[0]=="Generation"]
    gen_lst = [int(x.strip(".pkl")) for x in gen_lst]
    gen_lst.sort()
except ValueError:
    raise ReferenceError("There are no networks present to plot")

def load_gen(gen):
    gen_str = "Generation "+str(gen)+".pkl"
    gen_path = os.path.join(save_path, gen_str)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    nets = []
    file = open(gen_path, "rb")
    while True:
        try:
            nets.append(pickle.load(file))
        except EOFError:
            break
    file.close()
    nets = np.array(nets)
    try:
        nets = np.random.choice(nets, settings.number_nets, False)
    except:
        print("Insufficient saved nets. Taking Random Sample")
        nets = np.random.choice(nets, settings.number_nets, True)
    return nets

def find_fitnesses(nets):
    net_fitnesses = np.empty(settings.number_nets)
    for n, net in enumerate(nets):
        if net.fitness == None:
            fitnesses = [0. for _ in range(settings.repeats)]
            for r in range(settings.repeats):
                env = SSwingEnv.initialise()
                observation, env = SSwingEnv.stepper(*env, 0)
                for t in range(settings.max_steps):
                    output = net.output(observation)
                    action = output.index(max(output))
                    observation, env = SSwingEnv.stepper(*env, action)
                    reward = abs(observation[0])
                    fitnesses[r] += reward
            net.fitness = sum(fitnesses)/settings.repeats
        net_fitnesses[n] = net.fitness
    return net_fitnesses

min_fit = []
ave_fit = []
max_fit = []
for gen in gen_lst:
    nets = load_gen(gen)
    net_fitnesses = find_fitnesses(nets)
    min_fit.append(min(net_fitnesses))
    ave_fit.append(sum(net_fitnesses)/len(net_fitnesses))
    max_fit.append(max(net_fitnesses))
plt.plot()
plt.plot(gen_lst, max_fit, label="Highest Fitness")
plt.plot(gen_lst, ave_fit, label="Average Fitness")
plt.plot(gen_lst, min_fit, label="Lowest Fitness")
plt.xlim(min(gen_lst), max(gen_lst))
plt.xlabel("Generation")
plt.ylabel("Sum of Angles/radians")
plt.legend()
plt.show()
