from robot_interface import Robot
from encoder_interface import Encoders
import time
import numpy as np
import math

class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy)

        # Run code for set up of algorithm here e.g.
        self.speech.say("Setting up algorithm")
        self.speech.say("Time to swing")
        self.set_posture("seated")
        self.algorithm = self.algorithm_startup
        self.time_switch = 100
        self.decreasing = False
        self.pendulum_length = 2.0
        self.next_highest_angle  = None
        self.preious_av = None
        self.maintain_angle = 30


    def algorithm_startup(self, values):
        if values['time'] > 3 and -15 < values['be'] < 0 and values['av'] > 0:
            self.next_position = 'extended'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_time = values['time']
            self.preious_av = values['av']
            print('changing algorithm')
        if values['time'] > 3 and 0 < values['be'] < 15 and values['av'] < 0:
            self.next_position = 'seated'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_time = values['time']
            self.preious_av = values['av']
            print('changing algorithm')

    def algorithm_increase(self, values):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        current_av = values['av']
        current_be = values['be']

        if(np.sign(current_av) != np.sign(self.preious_av)):
            if(self.position == 'seated'):
                self.set_posture('extended')
            if(self.position == 'extended'):
                self.set_posture('seated')
        else:pass
        
        self.preious_av = current_av
        self.previous_be = current_be
        
        if(current_be >= self.maintain_angle+5):
            self.algorithm = self.algorithm_maintain

        
    def algorithm_maintain(self,values):
        current_av = values['av']
        current_be = values['be']
        if(np.sign(current_av) != np.sign(self.preious_av)):
            if(self.previous_be < self.maintain_angle):
                self.algorithm = self.algorithm_increase
            else:
                pass
        self.preious_av = current_av
        self.previous_be = current_be