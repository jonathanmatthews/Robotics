from robot_interface import Robot
from encoder_interface import Encoders
from numpy import sign
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
        #self.speech.say("Setting up algorithm")
        self.set_posture("extended")
        time.sleep(1.33)
        self.set_posture("seated")
        time.sleep(1.33)
        self.set_posture("extended")
        time.sleep(1.33)
        self.set_posture("seated")
        time.sleep(1.33)
        self.set_posture("extended")
        time.sleep(1.33)
        self.set_posture("seated")
        time.sleep(1.33)
        self.max_angle = 0


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
        #print time

        try:
    	  self.prev, self.curr = self.curr, self.b_encoder
    	  self.prev_time, self.curr_time = self.curr_time, time

    	except: # if don't exist yet
    	  self.prev, self.curr = 0, 0
    	  self.prev_time, self.curr_time = 0, 0

    	  self.max_times = [] # Times at which max/min amplitudes were reached.
    	  self.zero_times = []
    	  self.quarter_periods = []

    	if sign(self.curr) != sign(self.prev): # Zero point crossed.
    	  self.zero_times.append(time)

    	elif abs(self.curr) < abs(self.prev): # Pendulum is starting to move back.
    	  self.max_times.append(time)
    	  self.quarter_periods.append(self.max_times[-1] - self.zero_times[-1])