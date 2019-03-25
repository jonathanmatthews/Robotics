import matplotlib.pyplot as plt
import numpy as np
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file

output_data = '../Output_data/'
filenames = ['Box Masses', 'Box No Masses']

for filename in filenames:
    data = read_file(output_data + filename)

    t = data['time']
    be = data['be']

    plt.plot(t, be, label=filename)

plt.legend(loc='best')
plt.show()