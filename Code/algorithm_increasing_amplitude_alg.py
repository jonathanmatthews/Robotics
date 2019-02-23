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
        self.next_position = 'extended'

    def algorithm_startup(self, values):
        if values['time'] > 5 and values['be'] < 0 and values['be'] > -15 and values['av'] > 0:
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
        # sign of big encoder changes when crossing zero point
        if np.sign(current_be) != np.sign(self.previous_be):
            # record current time as the time it goes through the minimum
            self.min_time = values['time']

            # collect last 60 values of big encoder and time (be abs() so that minima become maxima)
            be = np.abs(self.all_data['be'][-60:])
            time = self.all_data['time'][-60:]

            # find indexes where maxima occur in big encoder absolute dataset
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            # extract time corresponding to latest maxima
            self.max_time = time[angle_max_index[-1]]

            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)
            # set time for position to switch
            # think it's actually best to switch late rather than early so no offset for time changing position
            self.time_switch = self.min_time + self.quart_period
            print self.quart_period, self.min_time, self.time_switch

        # at end of loop put current big encoder value as previous value
        self.previous_be = current_be
        # when time to switch comes change position
        if values['time'] >= self.time_switch:
            # change to new position
            current_pos = values['pos']
            if current_pos == 'seated':
                self.next_position = 'extended'
            elif current_pos == 'extended':
                self.next_position == 'seated'
            self.set_posture(self.next_position)
            # make sure doesn't try to keep on switching until value is reset in first if statement 
            self.time_switch += 100


