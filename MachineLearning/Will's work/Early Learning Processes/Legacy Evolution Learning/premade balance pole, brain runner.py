# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 13:34:03 2019

@author: William
"""
brain = brains[0]

observation = env.reset()
for t in range(10000):
    env.render()
    #print(observation)
    brain.update(observation)
    if brain.output < 0.5:
        action = 0
    else:
        action = 1
    observation, reward, done, info = env.step(action)
    if done:
        print(t)
        break

env.close()
