import numpy as np
from utility_functions import last_minima, zero_maxima, last_zero_crossing, moving_average, sign_zero
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter the data, and plot both the original and filtered signals.
def final_filter(time, values):

    # Filter requirements.
    order = 6
    fs = 1.0/np.mean(np.diff(time[-200:]))
    lowcut = 0.35 # desired cutoff frequency of the filter, Hz
    highcut = 0.65

    return time, butter_bandpass_filter(values, lowcut, highcut, fs, order)


class IncreaseAccelerometer():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))        


    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        times, filtered_az = final_filter(all_data['time'], all_data['az'])
        current_az = filtered_az[-1]
        previous_az = filtered_az[-2]

        if(sign_zero(previous_az)==-1 and previous_az - current_az <0):
            return 'seated'
        if(sign_zero(previous_az)==1 and previous_az - current_az >0):
            return 'extended'

        # switch conditions
        if values['time'] - self.start_time > self.duration:
            return 'switch'