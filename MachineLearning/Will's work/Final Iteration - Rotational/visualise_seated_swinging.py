# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

Visually runs the simulation with the best brain

@author: William
"""
import numpy as np
import settings
import pickle
import pygame
import os

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

env = SSwingEnv.initialise_display(False)
observation,env = SSwingEnv.stepper_display(*env, 0)
animation_path = os.path.join(os.getcwd(),"SSwingEnv Animation")
if not os.path.exists(animation_path):
    os.makedirs(animation_path)
r = 0
try:
    for t in range(settings.max_steps_long_run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
        output = net.output(observation)
        action = output.index(max(output))
        observation,env = SSwingEnv.stepper_display(*env, action)
        reward = abs(observation[0]+0.009)
        pygame.image.save(env[7], os.path.join(animation_path, "Frame{}.jpg".format(t)))
        print(observation, action)
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
