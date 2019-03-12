import numpy as np
import math


class IncreaseMaxAngle():

    def __init__(self, values, all_data, **kwargs):
        print 'Starting'
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.pendulum_length = 1.82
        self.min_angle = kwargs.get('min_angle', 5)
        self.next_highest_angle = None
        self.previous_max_angle = all_data['be'].max()
        self.offset = 0
        self.previous_1degree = None
        self.previous_1degree_time = None
        self.after_1degree = None
        self.after_1degree_time = None

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

        if(abs(previous_be)>1 and abs(current_av) <1):
            self.previous_1degree  = current_be
            self.previous_1degree_time = current_time
        if(abs(previous_be)<1 and abs(current_av) > 1):
            self.after_1degree = previous_be
            self.after_1degree_time = previous_time
                
        
        
        if (self.previous_1degree == None or  self.after_1degree == None):
            pass
        # If the sign changed, calculate the approximation of the highest point it can reach
        else:
            self.max_speed = math.radians(abs(self.previous_1degree - self.after_1degree)/abs(self.previous_1degree_time-self.after_1degree_time)) * self.pendulum_length
            h = 0.5*(self.max_speed**2)/9.8
            # Calculate the next highest angle in degrees,
            # The -2 degree at end is because we want to start change the position a little bit early
            self.next_highest_angle = math.degrees(
                math.acos((self.pendulum_length-h)/self.pendulum_length))+ self.offset
            self.next_highest_angle = np.sign(
                current_be) * self.next_highest_angle
            self.previous_1degree = None
            self.previous_1degree_time = None
            self.after_1degree = None
            self.after_1degree_time = None
            print values['time'], 'At lowest point', 'Big encoder {:.2f}'.format(values['be']) ,self.next_highest_angle
            
        if (self.next_highest_angle):
            next_pos = None

            if(np.sign(self.next_highest_angle) < 0 and current_be < self.next_highest_angle):
                if(self.increase == True):
                    print('seated')
                    next_pos = 'seated'
                else:
                    next_pos = 'extended'
            elif(np.sign(self.next_highest_angle) > 0 and current_be > self.next_highest_angle):
                if(self.increase == True):
                    print('extended')
                    next_pos = 'extended'
                else:
                    next_pos = 'seated'

            if(next_pos):
                self.next_highest_angle = None
                return next_pos

        if(np.sign(current_av) != np.sign(previous_av) and np.sign(previous_av) == -1):
            self.previous_max_angle = all_data['be'][-1]
            if(self.max_angle < abs(self.previous_max_angle) and self.increase == True):
                return 'switch'
            elif(abs(self.previous_max_angle) < self.min_angle and self.increase == False):
                return 'switch'
        if values['time'] - self.start_time > self.duration:
            return 'switch'
