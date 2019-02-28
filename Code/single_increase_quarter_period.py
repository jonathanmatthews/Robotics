from robot_interface import Robot
from encoder_interface import Encoders
import time as tme
import numpy as np


class IncreaseQuarterPeriod():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        self.time_switch = 100
        self.offset = -0.2
        self.max_angle = kwargs.get('max_angle', 50)
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.duration = kwargs.get('duration', 20)
        
        # using angular velocity to switch position
        if values['av'] < 0:
            self.next_position = 'seated'
        elif values['av'] > 0:
            self.next_position = 'extended'
        else:
            print 'ANGULAR VELOCITY EXACTLY ZERO'

    
    def algo(self, values, all_data):
        # sign of big encoder changes when crossing zero point
        if np.sign(values['be']) != np.sign(self.previous_be):

            self.min_time = self.last_zero_crossing(values)
            self.max_time = self.last_maxima(all_data)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            print self.time_switch

        if values['time'] > self.time_switch:
            # change to the new position
            # make sure it doesn't try to keep on switching until value is reset in first if statement
            self.time_switch += 100
            if self.next_position == 'seated':
                self.next_position = 'extended'
                return 'seated'
            else: 
                self.next_position = 'seated'
                return 'extended'

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']
      

    def last_zero_crossing(self, values):
        current_be = values['be']
        dt = values['time'] - self.previous_time

        interpolate = dt * np.abs(current_be) / \
            np.abs(current_be - self.previous_be)

        min_time = values['time'] - interpolate
        return min_time

    def last_maxima(self, all_data):
            be = np.abs(all_data['be'][-30:])
            time = all_data['time'][-30:]
            # extract time corresponding to latest maxima, index_max_angle(number of previous values to return)
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            max_time = time[angle_max_index[-1]]
            return max_time
 
