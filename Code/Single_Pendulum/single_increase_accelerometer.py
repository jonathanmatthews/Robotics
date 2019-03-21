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
    lowcut = 0.01 # desired cutoff frequency of the filter, Hz
    highcut = 0.65

    return time, butter_bandpass_filter(values, lowcut, highcut, fs, order)

class IncreaseAccelerometer():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        self.period = kwargs.get('period', 0.005)
        # offset is time from maximum to swing
        self.time_switch = 100
        self.offset = -0.4

        times, filtered_az = final_filter(all_data['time'], all_data['az'])
        self.min_time = last_minima(times, filtered_az, dt=self.period)
        self.last_maximum = zero_maxima('either', times, filtered_az, time_values='values', dt=self.period)

        self.checking_offset = 0.35
        self.check_time = self.min_time + 2 * abs(self.last_maximum - self.min_time) + self.checking_offset
        self.last_maximum -= 2.55/4.0
        # setting up times
        self.start_time = values['time']
        self.previous_time = values['time']

        # max_angle used for increasing min_angle for decreasing
        self.increasing = kwargs.get('increasing', True)
        self.max_angle = kwargs.get('max_angle', 180)
        self.min_angle = kwargs.get('min_angle', 5)
        
        # alternative switch condition
        self.duration = kwargs.get('duration', float('inf'))

        if self.increasing:
            print 'Increasing amplitude, quarter period'
        else:
            print 'Decreasing amplitude, quarter period'


    def algo(self, values, all_data):

        # sign of big encoder changes when crossing zero point
        if values['time'] > self.check_time:
            times, filtered_az = final_filter(all_data['time'], all_data['az'])
            self.min_time = last_minima(times, filtered_az, dt=self.period)
            self.max_time, self.last_maximum = zero_maxima('either', time_list=times, values_list=filtered_az, time_values='both', dt=self.period)
            self.max_time -= 2.55/4.0
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)
            self.check_time = self.min_time + 2 * self.quart_period + self.checking_offset
            print 'Ran at time {}'.format(values['time'])
            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            print 'Next switching time: {:.3f}'.format(self.time_switch), 'Last maximum: {:.3f}'.format(self.last_maximum)

        if values['time'] > self.time_switch:
            times, filtered_az = final_filter(all_data['time'], all_data['az'])
            last_maximum = zero_maxima('either', time_list=times, values_list=filtered_az, time_values='values', dt=self.period)
            self.time_switch += 100
            if last_maximum > 0:
                return 'extended'
            else:
                return 'seated'

        if values['time'] - self.start_time > self.duration:
            return 'switch'
