'''Stop algorithm that simply kicks, waits a half period,
    and kicks again. Calculates correct kicking order as will already be in 
    motion, and times starting kick to next maxima.'''

import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, next_position_calculation


class Stop():
    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', 10)
        self.stop_angle = kwargs.get('stop_angle', 1.0)
        self.wait_time = 1.25
        self.last_move = last_maxima(all_data, 'time')

        # sets up correct position
        av = values['av']
        if av >= 0:
            # positive angular momentum means going backward, therefore want seated to decrease
            self.start_pos = 'seated'
        else:
            # opposite of above
            self.start_pos = 'extended'
        print 'Stopping swing, constant period'

    def algo(self, values, all_data):
        t = values['time']

        if t > self.last_move + self.wait_time:
            print 'Stop swing', values['time']
            self.last_move = t
            return self.next_position(values)

        # ending if duration is over or minimum angle is reached
        if t - self.start_time > self.duration:
            print 'duration reached, stopping'
            return 'switch'
        if last_maxima(all_data, 'be') < self.stop_angle:
            print 'min angle reached, stopping'
            return 'switch'

    def next_position(self, values):
        if values['pos'] == 'seated':
            return 'extended'
        else:
            return 'seated'
