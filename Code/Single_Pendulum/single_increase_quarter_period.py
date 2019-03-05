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
        self.offset = -0.2
        # set up parameters
        self.start_time = values['time']
        self.previous_time = values['time']
        self.previous_be = values['be']

        # conditions for running, will stop at first condition reached 
        self.max_angle = kwargs.get('max_angle', 50)
        self.duration = kwargs.get('duration', 30)
        self.last_maximum = self.last_maxima(all_data, 'be')
        self.increasing = kwargs.get('increasing', True)
        if self.increasing == True:
            print 'Increasing amplitude, quarter period'
        else:
            print 'Decreasing amplitude, quarter period'
        self.min_angle = kwargs.get('min_angle', 6)

    
    def algo(self, values, all_data):
        # sign of big encoder changes when crossing zero point
        if np.sign(values['be']) != np.sign(self.previous_be):

            self.min_time = self.last_zero_crossing(values)
            self.max_time = self.last_maxima(all_data)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            self.last_maximum = self.last_maxima(all_data, 'be')
            print 'Next switching time', self.time_switch

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
        if values['time'] - self.start_time > self.duration:
            if self.increasing == True:
                print 'Switching from increasing, duration ended'
            else:
                print 'Switching from decreasing, duration ended'
            return 'switch'
        if (self.last_maximum > self.max_angle and self.increasing == True):
            print 'Maximum angle reached, switching'
            return 'switch'
        if (self.last_maximum < self.min_angle and self.increasing == False):
            print 'Minimum angle reached, switching'
            return 'switch' 
        return 'no change'
            
    def moving_average(self, values, window_size):
        ma = [np.sum(values[i:i+window_size])/window_size for i, _ in enumerate(values[:-window_size+1])]
        return ma


    def last_zero_crossing(self, values):
        current_be = values['be']
        dt = values['time'] - self.previous_time

        interpolate = dt * np.abs(current_be) / \
            np.abs(current_be - self.previous_be)

        min_time = values['time'] - interpolate
        return min_time

    def last_maxima(self, all_data, be_time='time'):
            # extracting a moving average of the previous encoder values to prevent incorrect maximas begin evaluated
            be = np.abs(self.moving_average(all_data['be'][-30:], 5))
            time = all_data['time'][-30:]
            # extract time corresponding to latest maxima, index_max_angle(number of previous values to return)
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            if be_time == 'time':
                return time[angle_max_index[-1]]
            elif be_time == 'be':
                return be[angle_max_index[-1]]

    def next_position_calculation(self, values):
        if values['be'] < 0 and self.increasing == True:
            next_position = 'seated'
        elif values['be'] > 0 and self.increasing == True:
            next_position = 'extended'
        elif values['be'] < 0 and self.increasing == False:
            next_position = 'extended'
        elif values['be'] > 0 and self.increasing == False:
            next_position = 'seated'
        else:
            print "CONDITIONS DON'T CORRESPOND TO ANY POSITION, POSITION KEEPING CONSTANT"
            next_position = values['pos']
        return next_position

class DecreaseQuarterPeriod(IncreaseQuarterPeriod):
    def __init__(self, values, all_data, **kwargs):
        IncreaseQuarterPeriod.__init__(self, values, all_data, **kwargs)
        
