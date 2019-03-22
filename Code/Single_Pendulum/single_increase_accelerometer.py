import numpy as np
from utility_functions import last_minima, zero_maxima, moving_average, sign_zero, last_maxima
from scipy.signal import butter, lfilter, freqz, filtfilt
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
    highcut = 0.50

    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    padded_signal = filtfilt(b, a, values)

    return padded_signal

def last_zero_crossing_az(time, filtered_az):
    current_az = filtered_az[-1]
    previous_az = filtered_az[-2]
    dt = time[-1] - time[-2]

    interpolate = dt * np.abs(current_az) / \
        np.abs(current_az - previous_az)

    min_time = time[-1] - interpolate
    return min_time

class IncreaseAccelerometer():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))        
        self.offset = 0.0
        self.period = kwargs.get('period', 0.005)

        self.filter_offset = 0.15
        self.time_switch = float('inf')

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        times = np.append(all_data['time'], np.array(values['time'])) + self.filter_offset
        az = np.append(all_data['az'], np.array(values['az']))

        # will collect the last n results
        n = int(1.0/self.period * 6.0)
        if n < 39:
            n = 40

        filtered_az = - final_filter(times[-n:], az[-n:])
        times = times[-n:]
        current_az = filtered_az[-1]
        previous_az = filtered_az[-2]

        if sign_zero(current_az) != sign_zero(previous_az):
            # print 'After {}'.format(current_az), 'Before {}'.format(previous_az)
            self.min_time = last_zero_crossing_az(times, filtered_az)
            self.max_time = last_maxima(times, filtered_az, time_values='time', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            print 'Next switching time: {:.3f}'.format(self.time_switch)

        if values['time'] > self.time_switch:
            self.time_switch = float('inf')
            return self.next_position_calculation(filtered_az)

        # switch conditions
        if values['time'] - self.start_time > self.duration:
            return 'switch'

    def next_position_calculation(self, filtered_az):
        if filtered_az[-1] < 0:
            return 'seated'
        elif filtered_az[-1] > 0:
            return 'extended'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"