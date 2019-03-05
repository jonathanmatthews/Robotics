import numpy as np
import matplotlib.pyplot as plt

def moving_average():
    x = all_data['time']
    #x = [1,2,3,4,5,6,7,8,9,10]
    #y = [1,3,5,9,11,14,15,12,17,22]
    y = all_data['be'][-30:]
    data = np.ma.average(y)
                
#average big encoder values over the last 5 values

    return data

# print moving_average()

def moving_average(values, window_size):
    # for i, value in enumerate(values[:-window_size]):
        # print np.sum(values[i:i+window_size])/window_size
    sum = [np.sum(values[i:i+window_size])/window_size for i, value in enumerate(values[:-window_size+1])]
    return sum

print moving_average_2([1.0, 3.0, 2.0, 5.0, 4.0, 8.0, 6.0, 22.0], 5)


