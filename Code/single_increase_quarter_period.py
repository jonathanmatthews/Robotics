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
        self.to_extended_offset = -0.2
        self.to_seated_offset = -0.2
        self.increasing = kwargs.get('increasing', True)
        self.max_angle = kwargs.get('max_angle', 50)
        self.previous_time = values['time']
        self.previous_be = values['be']
        
        # using angular velocity to switch position
        if values['av'] < 0 :
            self.next_position = 'extended'
        else:
            self.next_position = 'seated'

    
    def algo(self, values, all_data):
        
        current_be = values['be']
        current_time = values['time']
        dt = current_time - self.previous_time
        
        # sign of big encoder changes when crossing zero point
        if np.sign(current_be) != np.sign(self.previous_be):
            # record current time as the time it goes through the minimum
            interpolate = dt * np.abs(current_be) / \
                np.abs(current_be - self.previous_be)
                
            self.min_time = values['time'] - interpolate
            
            time = all_data['time'][-50:]
            # extract time corresponding to latest maxima, index_max_angle(number of previous values to return)
            self.index_max_angle(50, all_data)

            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)
            # set time for position to switch
            if values['pos'] == 'seated':
                self.time_switch = self.min_time + self.quart_period + self.to_extended_offset
            if values['pos'] == 'extended':
                self.time_switch = self.min_time + self.quart_period + self.to_seated_offset
            print self.time_switch
            # time_switch should be as near to the top as possible
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
        self.previous_be = current_be
        self.previous_time = current_time
      
 
    def index_max_angle(self, no_of_values, all_data):
        # collect the last 10 values of the big encoder and time (abs() will convert the minima to maxima).
        be = np.abs(all_data['be'][-no_of_values:])
        time = all_data['time'][-no_of_values:]
        #'print be
        # collect and find the indexes where maxima occur in big encoder absolute dataset
        angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            
        self.max_time = time[angle_max_index[-1]]
