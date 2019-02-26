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

        # Leans back slowly as to not disturb swing
        self.speech.say("Setting up algorithm")
        self.set_posture("extended", 0.1)
        self.b_max = 0
        self.b_min = 0
        self.event_number = 0
        self.algorithm = self.algorithm_start

    def algorithm_start(self, *args):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current posture
        """
        #aims to thrash about until the displacement is large enough (> 2 degrees)
        pos, t, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
        #Gets a running value of the max and min angles achieved
        if b_encoder > self.b_max:
            self.b_max = b_encoder
        if b_encoder < self.b_min:
            self.b_min = b_encoder
        print b_encoder, self.b_max, self.b_min
        
        ang_vel = self.get_ang_vel(self.event_number)
        
        if t > 0 and t < 0.1:
            self.set_posture("extended", 0.05)
            print "leaning back slowly"
        if t > 5.0 and t < 5.1:
            self.set_posture("seated", 1.0)
            print "leaning forward quickly"
        if t > 5.5 and t < 5.6:
            self.set_posture("extended", 1.0)
            print "leaning back quickly"
        if t > 6:
            if b_encoder < 0.8 * self.b_min and ang_vel < 0 and pos != "extended":
                self.set_posture("extended")
                print "extended"
            if b_encoder > 0.8 * self.b_max and ang_vel > 0 and pos != "seated":
                self.set_posture("seated")
                print "seated"
        
        # this switches algorithm after time is greater than 10
        if b_encoder > 2:
            self.algorithm = self.algorithm_increase

    def algorithm_increase(self, *args):
        pos, time, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
        print time, 'algo has changed'