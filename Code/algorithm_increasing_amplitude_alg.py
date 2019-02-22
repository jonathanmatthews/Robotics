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
        self.set_posture("extended")
        time.sleep(2)
        self.previous_be = 0
        self.algorithm = self.algorithm_startup
        self.next_position = 'seated'

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
        # print  np.sign(current_be) != np.sign(self.previous_be)
        if np.sign(current_be) != np.sign(self.previous_be):
            self.min_time = values['time']

            be = np.abs(self.all_data['be'][-60:])
            time = self.all_data['time'][-60:]
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            self.max_time = time[angle_max_index[-1]]

            self.quart_period = np.abs(self.min_time - self.max_time)
            self.time_switch = self.min_time + self.quart_period
            print self.quart_period, self.min_time, self.time_switch
        self.previous_be = current_be
        if values['time'] >= self.time_switch:
            self.set_posture(self.next_position)
            if values['pos'] == 'seated':
                self.next_position = 'seated'
            elif values['pos'] == 'extended':
                self.next_position = 'extended'
            self.time_switch += 2


