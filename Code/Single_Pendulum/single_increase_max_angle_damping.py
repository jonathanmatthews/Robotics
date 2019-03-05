import numpy as np
import math

class IncreaseDecrease():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 20)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', 20)
        self.min_angle = kwargs.get('min_angle', 5)
        self.previous_max_angle = all_data['be'].max()
        self.next_highest_angle = None
        self.pendulum_length = 1.82
        self.damping = 0.009
        self.g = 9.8
        self.mass_of_robot = 0.189
        self.damping_term_constant = ((self.damping/self.g)**0.5)*(np.pi*self.damping/(2*self.mass_of_robot))



    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        current_av = values['av']
        current_pos = values['pos']
        previous_av = all_data['av'][-1]
        current_be = values['be']
        previous_be = all_data['be'][-1]

        if(self.previous_max_angle and np.sign(current_be) != np.sign(previous_be)):
            print('At lowest point, calculating the next max angle!')
            self.max_speed = math.radians(values['av']) * self.pendulum_length
            cosx = 1-0.5*self.max_speed**2/(self.damping*self.g) - self.damping_term_constant*(math.sin(self.previous_max_angle))**2
            self.next_highest_angle = math.degrees(math.acos(cosx))-2
            print(self.next_highest_angle)
        
        if (self.next_highest_angle):
            next_pos = None

            if(np.sign(self.next_highest_angle) < 0 and current_be < self.next_highest_angle):
                if(self.increase == True):
                    next_pos = 'seated'
                elif(self.increase == False):
                    next_pos = 'extended'
            elif(np.sign(self.next_highest_angle) > 0 and current_be > self.next_highest_angle):
                if(self.increase == True):
                    next_pos = 'extended'
                elif(self.increase == False):
                    next_pos = 'seated'

            if(next_pos):
                self.next_highest_angle = None
                return next_pos

        if(np.sign(previous_av) != np.sign(current_av)):
            self.previous_max_angle = previous_be
    

        if(self.max_angle < abs(self.previous_max_angle) and self.increase == True):
            return 'switch'
        elif(abs(self.previous_max_angle) < self.min_angle and self.increase == False):
            return 'switch'
        if values['time'] - self.start_time > self.duration:
            return 'switch'