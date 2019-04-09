"""
Simple sigmoid function, was used in  a varriety of places
Doesn't really need its own file now but imports would need redoing.
"""

import numpy as np

def sigmoid(inp):
    output = 1/(1 + float(np.exp(-inp)))
    return output
