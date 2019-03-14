# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:18:18 2019

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

with open("net_python2.pkl", 'wb') as file:
    pickle.dump(net, file, protocol=2)
