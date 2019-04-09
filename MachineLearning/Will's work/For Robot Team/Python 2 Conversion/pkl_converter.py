# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:18:18 2019

Finds the best net in a pkl and converts it to a text document network_python2 can read
Run in python 3

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

strng = ""
for layer in net.nodes:
    for node  in layer:
        strng += "Node(self, {}, [".format(node.bias)
        for link in node.links:
            strng += "({}, {}),".format(link.connection, link.weight)
        strng += "])\n"
    strng += "\n"

with open("net_data.txt", "w") as file:
    file.write(strng)
