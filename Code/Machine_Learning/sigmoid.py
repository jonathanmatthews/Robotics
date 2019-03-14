import numpy as np

def sigmoid(inp):
    output = 1/(1 + float(np.exp(-inp)))
    return output
