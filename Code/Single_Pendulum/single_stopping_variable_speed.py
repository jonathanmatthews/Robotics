'''Stop algorithm that simply kicks, waits a half period,
    and kicks again. Calculates correct kicking order as will already be in 
    motion, and times starting kick to next maxima.'''



import numpy as np
from utility_functions import last_maxima, last_zero_crossing, moving_average, sign_zero

class StoppingVariableSpeed():
    def __init__(self, values, all_data, **kwargs):
        self.period = kwargs.get('period', 0.005)
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))

        self.wait_time = 20
        self.last_move = last_maxima(all_data['time'], all_data['be'], time_values='time', dt=self.period)
        self.offset = -0.2

        # offset is time from maximum to swing
        self.time_switch = 50

        self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)

        # setting up times
        self.previous_time = values['time']
        self.previous_be = values['be']

        # max_angle used for increasing min_angle for decreasing
        self.increasing = kwargs.get('increasing', True)
        self.max_angle = kwargs.get('max_angle', 180)
        self.min_angle = kwargs.get('min_angle', 5)



        # sets up correct position
        av = values['av']
        if av >= 0:
            # positive angular momentum means going backward, therefore want seated to decrease
            self.next_pos = 'extended'
        else:
            # opposite of above
            self.next_pos = 'seated'
        print 'Stopping swing, constant period'
        
        

    #def algo(self, values, all_data):
        #t = values['time']
        #max_encoder_angle = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)
        
        #speed = abs(max_encoder_angle*0.1)
        
    
        #if speed < 0.1:
            #speed = 0.1
            #return speed
        #if t > self.last_move + self.wait_time + self.offset:
            #print 'Last maxima {}'.format(abs(max_encoder_angle))
            #print 'Stop swing', values['time']
            #self.last_move = t
            #return self.next_position(speed)

        ## ending if duration is over or minimum angle is reached
        #if t - self.start_time > self.duration:
            #print 'duration reached, stopping'
            #return 'switch'
        #if abs(max_encoder_angle) < self.min_angle:
            #print 'min angle reached, stopping'
            #return 'switch'
    
    def algo(self, values, all_data):
        max_encoder_angle = last_maxima(all_data['time'], all_data['be'], time_values='values', dt=self.period)
        
        speed = abs(max_encoder_angle*0.1)
        if speed > 0.8:
            speed = 0.8
            return speed
        if speed < 0.05:
            speed = 0.05
            return speed
        '''sign of big encoder changes when crossing zero point'''
        if sign_zero(values['be']) != sign_zero(self.previous_be):
            print 'After {}'.format(values['be']), 'Before {}'.format(self.previous_be)

            self.min_time = last_zero_crossing(values, self.previous_time, self.previous_be)
            self.max_time, self.last_maximum = last_maxima(all_data['time'], all_data['be'], time_values='both', dt=self.period)
            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)

            print 'Ran at time {}'.format(values['time'])
            # set time for position to switch
            self.time_switch = self.min_time + self.quart_period + self.offset
            print 'Next switching time: {:.3f}'.format(self.time_switch), 'Last maximum: {:.3f}'.format(self.last_maximum)

        # At the end of the loop, set the value of big encoder to the previous value
        self.previous_be = values['be']
        self.previous_time = values['time']

        if values['time'] > self.time_switch:
            self.time_switch += 50
            return self.next_position(speed)

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
    def next_position(self, speed):
        if self.next_pos == 'seated':
            self.next_pos = 'extended'
            return ['seated', speed]
        else:
            self.next_pos = 'seated'
            return ['extended', speed]
