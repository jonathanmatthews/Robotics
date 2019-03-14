# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pickle

with open("net_python2.pkl", 'rb') as file_n:
    net = pickle.load(file_n)
print(net.output([1, 0.5, 0.5]))
