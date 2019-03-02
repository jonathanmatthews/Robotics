from robot_interface import Robot
from encoder_interface import Encoders
import time as tme
import numpy as np


class Nothing():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', 20)

    
    def algo(self, values, all_data):
        print 'Nothing', values['time']

        if values['time'] - self.start_time > self.duration:
            return 'switch'
        
