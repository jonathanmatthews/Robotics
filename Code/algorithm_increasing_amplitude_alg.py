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
        print self.get_acc()
        self.set_posture("seated")
        self.algorithm = self.algorithm_startup
        self.time_switch = 100
        self.to_extended_offset = 0.0
        self.to_seated_offset = 0.0
        self.decreasing = False


    def algorithm_startup(self, values):
        if values['time'] > 3 and -15 < values['be'] < 0 and values['av'] > 0:
            self.next_position = 'extended'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_time = values['time']
        if values['time'] > 3 and 0 < values['be'] < 15 and values['av'] < 0:
            self.next_position = 'seated'
            self.algorithm = self.algorithm_increase
            self.previous_be = values['be']
            self.previous_time = values['time']

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
        current_time = values['time']
        dt = current_time - self.previous_time
        # sign of big encoder changes when crossing zero point
        if np.sign(current_be) != np.sign(self.previous_be):
            interpolate = dt * np.abs(current_be) / np.abs(current_be - self.previous_be)
            # record current time as the time it goes through the minimum
            self.min_time = values['time'] - interpolate

            # collect last 60 values of big encoder and time (be abs() so that minima become maxima)
            be = np.abs(self.all_data['be'][-10:])
            time = self.all_data['time'][-10:]

            # find indexes where maxima occur in big encoder absolute dataset
            angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1
            # extract time corresponding to latest maxima
            self.max_time = time[angle_max_index[-1]]

            # quarter period difference between time at maxima and minima
            self.quart_period = np.abs(self.min_time - self.max_time)
            # set time for position to switch
            # think it's actually best to switch late rather than early so no offset for time changing position
            if values['pos'] == 'seated':
                self.time_switch = self.min_time + self.quart_period + self.to_extended_offset
            if values['pos'] == 'extended':
                self.time_switch = self.min_time + self.quart_period + self.to_seated_offset
            print self.time_switch

        # at end of loop put current big encoder value as previous value
        self.previous_be = current_be
        self.previous_time = current_time
        # want time to switch as close to top as possible
        if np.abs(values['time'] - self.time_switch) <= dt/2:
            # when it is decreasing stop doing anything at 2 degrees
            if np.abs(values['be']) < 2:
                pass
            # first time it is 20 degrees or more it will skip a cycle so that motion is opposite and amplitude decreases
            elif np.abs(values['be']) < 65 or self.decreasing == True:
                # change to new position
                if self.next_position == 'seated':
                    self.set_posture(self.next_position)
                    self.next_position = 'extended'
                elif self.next_position == 'extended':
                    self.set_posture(self.next_position)
                    self.next_position = 'seated'
                # make sure doesn't try to keep on switching until value is reset in first if statement 
                self.time_switch += 100
            elif np.abs(values['be']) >= 65:
                self.decreasing = True
