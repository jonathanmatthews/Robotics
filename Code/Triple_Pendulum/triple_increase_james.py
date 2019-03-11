from time import time

import time as tme
import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, position_seat_cartesian


class TripleIncreaseQuarterPeriod():

    def total_angle(self, be, se0, se1):
        x, y = position_seat_cartesian(be, se0, se1)
        return np.arctan(x/y) * 180/np.pi

    def last_maxima(self, all_data, ta_time='time', window_size=5):
        times = all_data['time']
        be = all_data['be']
        se0 = all_data['se0']
        se1 = all_data['se1']
        ta = [self.total_angle(*values) for values in zip(be, se0, se1)]
        avg_ta = np.abs(moving_average(ta[-500:], window_size))
        angle_max_index = (np.diff(np.sign(np.diff(avg_ta))) < 0).nonzero()[0] + 1 + (window_size - 1)/2
        if ta_time == 'time':
            return times[-500:][angle_max_index[-1]]
        elif ta_time == 'ta':
            return ta[-500:][angle_max_index[-1]]



    def __init__(self, values, all_data, **kwargs):
        # offset is time from maximum to swing
        self.time_switch = 1000
        self.offset = -0.2
        self.last_maximum = self.last_maxima(all_data, 'ta')

        # setting up times
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_ta = self.total_angle(values['be'], values['se0'], values['se1'])

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
        current_ta = self.total_angle(values['be'], values['se0'], values['se1'])
        if np.sign(current_ta) != np.sign(self.previous_ta):

            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_ta)
            self.max_time = last_maxima(all_data, be_time='time')
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            self.last_maximum = last_maxima(all_data, be_time='be')
            print 'Next switching time', self.time_switch

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_ta = current_ta
        self.previous_time = values['time']

        if values['time'] > self.time_switch:
            self.time_switch += 100
            return self.next_position_calculation(values)

        return self.end_conditions(values)

    def end_conditions(self, values):
        # either conditions met
        if values['time'] - self.start_time > self.duration:
            if self.increasing == True:
                print 'Switching from increasing, duration ended'
            else:
                print 'Switching from decreasing, duration ended'
            return 'switch'
        if (abs(self.last_maximum) > self.max_angle and self.increasing == True):
            print 'Maximum angle reached, switching'
            return 'switch'
        if (abs(self.last_maximum) < self.min_angle and self.increasing == False):
            print 'Minimum angle reached, switching'
            return 'switch'
        return 'no change'

    def next_position_calculation(self, values):
        ta = self.total_angle(values['be'], values['se0'], values['se1'])
        if ta < 0 and self.increasing == True:
            next_position = 'seated'
        elif ta > 0 and self.increasing == True:
            next_position = 'extended'
        elif ta < 0 and self.increasing == False:
            next_position = 'extended'
        elif ta > 0 and self.increasing == False:
            next_position = 'seated'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"
            next_position = values['pos']
        return next_position


class DecreaseQuarterPeriod(TripleIncreaseQuarterPeriod):
    def __init__(self, values, all_data, **kwargs):
        IncreaseQuarterPeriod.__init__(self, values, all_data, **kwargs)
