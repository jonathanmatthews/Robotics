# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 17:58:42 2019

@author: William
"""
import pickle
import numpy as np

nets = []
file = open("nets_python3.pkl", "rb")
while True:
    try:
        nets.append(pickle.load(file))
    except EOFError:
        break
file.close()

nets = np.array(nets)
net_fits = np.array([net.fitness for net in nets])

net = nets[np.argmax(net_fits)]

def function(inputs):
    output = net.output(inputs)
    action = output.index(max(output))
    return action
