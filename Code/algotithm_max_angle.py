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
        self.to_extended_offset = 0.0
        self.to_seated_offset = 0.0
        self.decreasing = False
        self.pendulum_length = 2.0
        self.next_highest_angle  = None
        self.max_speed = None
        self.maintain_angle = 30
        self.previous_av = None


    def algorithm_startup(self, values):
        if values['time'] > 3 and -15 < values['be'] < 0 and values['av'] > 0:
            self.next_position = 'extended'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_av = values['av']
        if values['time'] > 3 and 0 < values['be'] < 15 and values['av'] < 0:
            self.next_position = 'seated'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_av = values['av']

    def algorithm_increase(self, values):
        """
        Use the max_angle approximation to estimate the time to switch the position
        """
        current_be = values['be']
        current_posture = values['pos']
        current_av = values['av']
        
        #Check if the sign of the big encoder data has changed
        #If not changed, we know the swing is not at its lowest point
        if (np.sign(self.previous_be) == np.sign(current_be)):
            pass
        #If the sign changed, calculate the approximation of the highest point it can reach
        else:
            print("At lowest point now, calculating the next max angle")
            self.max_speed = values['av']
            h = 0.5*(self.max_speed**2)/9.8
            #Calculate the next highest angle in degrees, 
            #The -2 degree at end is because we want to start change the position a little bit early
            self.next_highest_angle = math.degrees(math.acos((self.pendulum_length-h)/self.pendulum_length))-2
            print(r'The next highest angle is {self.next_highest_angle}')
        
        self.previous_be = current_be
        self.previous_av = current_av

        if (self.next_highest_angle):
             if (abs(current_be)>self.next_highest_angle):
                 if(current_posture == 'extended'):
                     next_pos = 'seated'
                 else:
                     next_pos = 'extended'
                 self.set_posture(next_pos)
                 self.next_highest_angle = None
        
        if(current_be >= self.maintain_angle+5):
            self.algorithm = self.algorithm_maintain
    
    def algorithm_maintain(self,values):
        current_av = values['av']
        current_be = values['be']
        if(np.sign(current_av) != np.sign(self.previous_av)):
            if(self.previous_be < self.maintain_angle):
                self.algorithm = self.algorithm_increase
            else:
                pass
        self.preious_av = current_av
        self.previous_be = current_be



             

