from robot_interface import Robot
from encoder_interface import Encoders
import time as tme
import numpy as np


class MaintainConstant():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        # conditions for running, will stop at first condition reached 
        self.max_angle = kwargs.get('max_angle', 10)
        self.duration = kwargs.get('duration', float('inf'))


    def algo(self, values, all_data):
        print 'Maintain'
        if values['be'] > self.max_angle - 3.0:
            print values['be']
            return 'extended'
        if values['be'] < -self.max_angle + 3.0:
            print values['be']
            return 'seated'
        
        if values['time'] - self.start_time > self.duration:
            return 'switch'
        
