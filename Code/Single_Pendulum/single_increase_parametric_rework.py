import numpy as np
from numpy import sign
from utility_functions import last_maxima


class Increase():

    def __init__(self, values, all_data, **kwargs):
        """
        Set up the parameters for parametric pumping.
        """
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increasing = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float("inf"))
        self.prev_be = values['be']
        self.prev_time = values['time']
        self.min_offset = -0.35
        self.max_offset = -0.35
        self.next_max = values['time'] + 100
        self.next_min = values['time'] + 100

    def algo(self, values, all_data, **kwargs):

        if sign(values['be']) != sign(self.prev_be):

            # calculate true zero crossing point
            dt = values['time'] - self.prev_time
            interpolate = dt * np.abs(values['be']) / \
                np.abs(values['be'] - self.prev_be)
            true_zero_time = values['time'] - interpolate

            # calculate quarter period based on latest maximum and minimum
            self.max_times = last_maxima(all_data, be_time='time')
            quarter_period = np.abs(self.max_times[-1] - true_zero_time)

            # maximum and minimum point
            self.next_max = true_zero_time + quarter_period + self.max_offset
            self.next_min = true_zero_time + 2 * quarter_period + self.min_offset
            print values['time'], self.next_max, self.next_min

        self.prev_be = values['be']
        self.prev_time = values['time']

        # if time to switch change to correct position
        if values['time'] > self.next_max:
            self.next_max += 100
            if self.increasing:
                return 'lowered'
            else:
                return 'raised'
        if values['time'] > self.next_min:
            self.next_min += 100
            if self.increasing == False:
                return 'raised'
            else:
                return 'lowered'

        # switch if angle is big enough or duration is over
        if values['time'] - self.start_time > self.duration:
            return 'switch'
        if values['be'] > self.max_angle:
            return 'switch'
