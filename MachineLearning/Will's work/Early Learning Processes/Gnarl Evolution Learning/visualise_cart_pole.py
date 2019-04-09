# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

@author: William
"""
import numpy as np
import gym
import settings
import pickle
import os

from premade_balance_pole import CartPoleEnv

save_path = os.path.join(os.getcwd(),"CartPoleEnv")
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

env = CartPoleEnv()
#env = gym.make('CartPole-v1')
#env._max_episode_steps = settings.max_steps*10
observation = env.reset()
r = 0
try:
    for t in range(settings.max_steps*10):
        env.render()
        #print(observation)
        output = net.output(observation)
        action = output.index(max(output))
        observation, reward, done, info = env.step(action)
        print(observation, output, action)
        r += reward
        if done:
            print(r)
            print()
            #print(net.nodes)
            print(net.fitness)
            break
    else:
        print(r)
        print()
        #print(net.nodes)
        print(net.fitness)

    env.close()

except KeyboardInterrupt:
    print(r)
    print()
    print(net.nodes)
    print(net.fitness)
    env.close()
