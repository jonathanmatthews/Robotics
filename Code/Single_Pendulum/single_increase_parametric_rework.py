import numpy as np
from numpy import sign

class Increase():

    def __init__(self, values, all_data, **kwargs):
        """
        Set up the parameters for parametric pumping.
        """
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float("inf"))
        self.decrease = kwargs.get('decrease', False)
        self.prev_be = values['be']
        self.prev_time = values['time']
        self.min_offset = -0.35
        self.max_offset = -0.35
        self.next_max = values['time'] + 100
        self.next_min = values['time'] + 100

    
    def last_maxima(self, all_data):
        """
        Obtain the time of the last maxima, on either side of the swing.
        """
        be = np.abs(all_data['be'][-30:])
        time = all_data['time'][-30:]
        
        angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1 # Obtain index.
        max_times = time[angle_max_index]

        return max_times
    
    def algo(self, values, all_data, **kwargs):
        
        if sign(values['be']) != sign(self.prev_be):

            dt = values['time'] - self.prev_time
            interpolate = dt * np.abs(values['be']) / \
                np.abs(values['be'] - self.prev_be)
            true_zero_time = values['time'] - interpolate

            self.max_times = self.last_maxima(all_data)
            quarter_period = np.abs(self.max_times[-1] - true_zero_time)

            self.next_max = true_zero_time + quarter_period + self.max_offset
            self.next_min = true_zero_time + 2 * quarter_period + self.min_offset
            print values['time'], self.next_max, self.next_min

        self.prev_be = values['be']
        self.prev_time = values['time']
        
        if values['time'] > self.next_max:
            self.next_max += 100
            return 'lowered'
        if values['time'] > self.next_min:
            self.next_min += 100
            return 'raised'
