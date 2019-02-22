from robot_interface import Robot
from encoder_interface import Encoders
import time

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
        self.speech.say("\\rspd=100\\Time to swing")
        self.set_posture("seated")
        time.sleep(2)
        self.set_posture("extended")


        print 2
        self.max_angle = 0
        self.algorithm = self.algorithm_start

    def algorithm_start(self, *args):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        pos, time, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
        print time
        # this switches algorithm after time is greater than 10
        if time > 10:
            self.algorithm = self.algorithm_increase

    def algorithm(self, *args):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        pos, time, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
        if b_encoder < -self.max_angle + 1 and pos == 'extended':
            self.set_posture('seated')
            self.max_angle = abs(b_encoder)
        if b_encoder > self.max_angle - 1 and pos == 'seated':
            self.set_posture('extended')
            self.max_angle = abs(b_encoder)
        print time, b_encoder, self.max_angle
