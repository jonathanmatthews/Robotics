# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

@author: William
"""
from brain import Brain #analysis:ignore
from config import Config
import gym #analysis:ignore
from numpy import array #analysis:ignore
import os

from premade_balance_pole import CartPoleEnv

settings = Config()

save_path = os.path.join(os.getcwd(),settings.env_name)
oldest_gen = max([int(x.split(" ")[1]) for x in os.listdir(save_path)])
oldest_str = "Generation "+str(oldest_gen)
gen_path = os.path.join(save_path, oldest_str)

nets = os.listdir(gen_path)
net_fits = [float(x.split(" ")[-1].split(".")[0]) for x in nets]

brain_path = nets[net_fits.index(max(net_fits))]

path = os.path.join(gen_path, brain_path)
with open(path, "r") as file:
    file_string = ""
    for line in file:
        file_string += line
brain = eval(file_string)

env = CartPoleEnv()
#env = gym.make(settings.env_name)
#env._max_episode_steps = settings.vis_steps+1
observation = env.reset()
r = 0
try:
    for t in range(settings.vis_steps):
        env.render()
        #print(observation)
        action = brain.output(observation)
        observation, reward, done, info = env.step(action)
        print(observation, action)
        r += reward
        if done:
            print(r)
            break
    else:
        print(r)

    env.close()

except KeyboardInterrupt:
    print(r)
    env.close()
