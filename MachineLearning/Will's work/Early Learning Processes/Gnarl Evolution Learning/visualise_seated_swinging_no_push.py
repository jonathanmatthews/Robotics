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

import Seated_Swinging_no_push_ML_Display as SSwingEnv

save_path = os.path.join(os.getcwd(),"SSwingNoPushEnv")
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
try:
    for t in range(settings.max_steps*1):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
        output = net.output(observation)
        action = output.index(max(output))
        observation,env = SSwingEnv.stepper(*env, action)
        print(observation, action)
        reward = abs(observation[0])
        r += reward
    print(r)
    print()
    #print(net.nodes)
    print(net.fitness)
    pygame.display.quit()
    pygame.quit()

except KeyboardInterrupt:
    print(r)
    print()
    #print(net.nodes)
    print(net.fitness)
    pygame.display.quit()
    pygame.quit()
