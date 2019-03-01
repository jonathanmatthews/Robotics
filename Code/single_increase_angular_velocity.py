from time import time
import numpy as np

class IncreaseDecrease():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = time()
        self.max_angle = kwargs.get('max_angle', 20)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', 20)
        self.min_angle = kwargs.get('min_angle',5)
        self.previous_max_angle = all_data['be'].max()



    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        current_av = values['av']
        current_pos = values['pos']
        previous_av = all_data['av'][-1]
        if(self.increase == True):
            if(np.sign(current_av) != np.sign(previous_av)):
                self.previous_max_angle = all_data['be'][-1]
                if(current_pos  == 'seated'):
                    return 'extended'
                elif(current_pos == 'extended'):
                    return 'seated'
            else:
                pass
        elif(self.increase == False):
            if(np.sign(current_av) != np.sign(previous_av) and np.sign(previous_av) == -1):
                self.previous_max_angle = all_data['be'][-1]
                return 'extended'
            elif(np.sign(current_av) != np.sign(previous_av) and np.sign(previous_av) == 1):
                self.previous_max_angle = all_data['be'][-1]
                return 'seated'
        if(all_data['be'][-1]>self.max_angle):
            print('switch algorithm from single_increase_angular_velocity')
            return 'switch'

        if(self.increase == True):
            print 'Increase', values['time']
            if abs(values['be']) > self.max_angle:
                return 'switch'
        elif(self.increase == False):
            print 'Decrease', values['time']
            if abs(self.previous_max_angle) < self.min_angle:
                return 'switch'
        if time() - self.start_time > self.duration:
            return 'switch'