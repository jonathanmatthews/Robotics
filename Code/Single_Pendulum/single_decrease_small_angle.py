import numpy as np
import math


class DecreaseSmallAngle():

    def __init__(self, values, all_data, **kwargs):
        print 'Starting'
        self.start_time = values['time']
        self.max_speed = kwargs.get('max_speed', 1)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.pendulum_length = 1.82
        self.min_angle = kwargs.get('min_angle', 1)
        self.next_highest_angle = None
        self.previous_left_max_angle = all_data['be'].max()
        self.previous_right_max_angle = all_data['be'].max()
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

        if(np.sign(current_be)!= np.sign([previous_be])):
            if( (current_be-previous_be)<0 and values['pos'] == 'seated'):
                return ['extended', self.max_speed]
            elif( (current_be-previous_be)>0 and values['pos'] == 'extended'):
                return ['seated',self.max_speed]
        
        if(np.sign(previous_be)==-1 and previous_be - current_be <0):
            self.previous_max_left_angle = previous_be
            print('max_angle',previous_be)
        elif(np.sign(previous_be)==1 and previous_be - current_be >0):
            self.previous_max_right_angle = previous_be
            print('max_angle',previous_be)

        if(abs(self.previous_left_max_angle)<self.min_angle and abs(self.previous_right_max_angle )<self.min_angle):
            return 'switch'
        
        av_list = []
        
        for x in range(20):
            if(all_data['av'][-x] == 0):
                av_list.append(True)
            else:
                av_list.append(False)
        
        if(False in av_list):
            pass
        else:
            if(abs(current_be)>1):
                pass
            else:
                return 'switch'
        
