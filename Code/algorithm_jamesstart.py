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

        # Leans back slowly as to not disturb swing
        self.speech.say("Setting up algorithm")
        self.speech.say("Here we go ooooooo")
        self.set_posture("extended", 0.05)

        self.b_max = 0
        self.b_min = 0
        self.event_number = 0
        self.algorithm = self.algorithm_start

    def algorithm_start(self, values):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current posture
        """
        #aims to thrash about until the displacement is large enough (> 2 degrees)
        t = values["time"]
        be = values["be"]
        
        if values["be"] > self.b_max:
            self.b_max = values["be"]
        if values["be"] < self.b_min:
            self.b_min = values["be"]
        print values["be"], self.b_max, self.b_min
        
        ang_vel = self.get_ang_vel(values["time"], values["be"])

        if t > 1.0 and t < 1.1:
            self.set_posture("seated", 1.0)
            print "leaning forward quickly"
        if t > 1.3 and t < 1.4:
            self.set_posture("extended", 1.0)
            print "leaning back quickly"
        if t > 1.8:
            if be < 0.8 * self.b_min and ang_vel < 0 and pos != "extended":
                self.set_posture("extended")
                print "extended"
            if be > 0.8 * self.b_max and ang_vel > 0 and pos != "seated":
                self.set_posture("seated")
                print "seated"
        
        # this switches algorithm after time is greater than 10
        if be > 1:
            self.algorithm = self.algorithm_increase

    def algorithm_increase(self, values):
        print time, 'algo has changed'