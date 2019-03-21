import numpy as np
import math
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero

class IncreaseMaxAngle():

    def __init__(self, values, all_data, **kwargs):
        self.period = kwargs.get('period', 0.005)
        # offset is time from maximum to swing
        self.time_switch = 100
        self.offset = -0.1
        self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.pendulum_length = 1.82
        self.min_angle = kwargs.get('min_angle', 0.5)
        self.next_highest_angle = None
        self.previous_max_angle = all_data['be'].max()
        self.offset = 0
        self.quart_period = 0.75

    def algo(self, values, all_data):
        """
        Use the max_angle approximation to estimate the time to switch the position
        """
        current_be = values['be']
        previous_be = all_data['be'][-1]
        current_av = values['av']
        previous_av = all_data['av'][-1]
        current_time = values['time']
        previous_time = all_data['time'][-1]
        print 'Max angle','Time: {:.2f}'.format(values['time']), 'Big encoder value: {:.2f}'.format(values['be'])
        # sign of big encoder changes when crossing zero point
        if sign_zero(values['be']) != sign_zero(previous_be):
            print 'After {}'.format(values['be']), 'Before {}'.format(previous_be)

            self.min_time = last_zero_crossing(values, previous_time, previous_be)
            self.max_time, self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='both', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time) + self.offset
        if(np.sign(current_be)!= np.sign([previous_be])):
            if(current_be<0 and values['pos'] != 'extended'):
                return ['seated', 0.3/self.quart_period]
            elif(current_be > 0 and values['pos'] != 'seated'):
                return ['extended',0.3/self.quart_period]
        
        if(np.sign(previous_be)==-1 and previous_be - current_be <0):
            self.previous_max_angle = previous_be
            print('max_angle',previous_be)
        elif(np.sign(previous_be)==1 and previous_be - current_be >0):
            self.previous_max_angle = previous_be
            print('max_angle',previous_be)

        if(self.previous_max_angle<self.min_angle):
            return 'switch'