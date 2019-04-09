# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:21:14 2019

@author: William
"""
from sigmoid import sigmoid
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-6,6,1000)
y = np.array([sigmoid(i) for i in x])

plt.figure()
plt.plot(x, y)
plt.vlines(0, 0, 1.05)
plt.hlines(0, min(x), max(x))
plt.xlim(min(x), max(x))
plt.ylim(-0.05, 1.05)
plt.show()
