from robot_interface import Robot
from encoder_interface import Encoders
import time
import numpy as np

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
        time.sleep(2)
        self.previous_be = 0
        self.algorithm = self.algorithm_startup

    def algorithm_startup(self, values):
        if values['time'] > 5:
            self.algorithm = self.algorithm_increase

    def algorithm_increase(self, values):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        current_be = values['be']
        if np.sign(current_be) != np.sign(self.previous_be):
            self.min_time = values['time']

            be = self.all_data['be'][-40:]
            time = self.all_data['time'][-40:]
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            self.max_time = time[angle_max_index[-1]]

            self.quart_period = np.abs(self.min_time - self.max_time)
            print self.quart_period
        self.previous_be = current_be