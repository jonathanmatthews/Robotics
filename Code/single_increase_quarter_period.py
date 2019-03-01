from robot_interface import Robot
from encoder_interface import Encoders
import time as tme
import numpy as np


class IncreaseQuarterPeriod():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        # stops switching too often
        self.time_switch = 100
        # how far from calculated top nao swings at
        self.offset = 0.0
        # conditions for running, will stop at first condition reached 
        self.max_angle = kwargs.get('max_angle', 50)
        self.duration = kwargs.get('duration', 20)

        # set up parameters
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']
        self.increasing = kwargs.get('increasing', True)

    
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

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']
      
        if values['time'] > self.time_switch:
            # don't want nao to trigger every cycle so set next time far ahead, it will be reset when zero point is crossed
            self.time_switch += 100
            position_to_change = self.next_position_calculation(values)
            # return string corresponding to position to change to, interface then handles changing
            return position_to_change
        
        # either conditions met
        if values['time'] - self.start_time > self.duration or values['be'] > self.max_angle:
            return 'switch'
        return 'no change'
            

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
 
    def next_position_calculation(self, values):
        print 'Big encoder at evaluation', values['be']
        if values['be'] < 0 or values['av'] < 0 and self.increasing == True:
            next_position = 'seated'
        elif values['be'] > 0 or values['av'] > 0 and self.increasing == True:
            next_position = 'extended'
        elif values['be'] < 0 or values['av'] < 0 and self.increasing == False:
            next_position = 'extended'
        elif values['be'] > 0 or values['av'] > 0 and self.increasing == False:
            next_position = 'seated'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"
            next_position = values['pos']
        return next_position
        
