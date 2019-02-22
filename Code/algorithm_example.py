from robot_interface import Robot
from encoder_interface import Encoders


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
        self.set_posture("seated")

        self.algorithm = self.algorithm_start

    def algorithm_start(self, values):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        time = values['time']
        # print time
        # this switches algorithm after time is greater than 10
        if time > 5:
            self.algorithm = self.algorithm_increase
        print self.all_data['time']
        print time

    def algorithm_increase(self, values):
        time = values['time']
        print self.all_data['time']
        print time, 'algo has changed'
