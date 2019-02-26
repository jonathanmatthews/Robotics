from robot_interface import Robot
from encoder_interface import Encoders
from numpy import sign


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

        # Parametric not able to start swing from 0 amplitude,
        # so need rotating swinging to start.

        if time > -1:
            self.algorithm = self.algorithm_increase
        

    def algorithm_increase(self, values):
        """
        Define parametric swinging function, for current swing state 'values'.
        See interface.py for details.
        """

        TOLERANCE = 0 # How many seconds early the robot is allowed to switch positions.


        ### Getting period:

        try:
            # Shuffle values around, such that we compare the current state to
            # the previous state.

            self.prev, self.curr = self.curr, self.get_big_encoder
            self.prev_time, self.curr_time = self.curr_time, values['time']
        
        except: # If this is the first time this function is run.
            self.prev, self.curr = 0, 0
            self.prev_time, self.curr_time = 0, 0

            self.max_times = [] # Times at which max amplitude reached.
            self.zero_times = [] # Times at which zero point was reached.
            self.quarter_periods = []
        
        if sign(self.curr) != sign(self.prev): # Zero crossed
            self.zero_times.append(values['time'])
            self.moving_down = False
        
        elif abs(self.curr) < abs(self.prev) and not self.moving_down:
            self.max_times.append(values['time'])
            self.moving_down = True

            # Moving down flag prevents max_times from being appended to more than once.
            
            quarter_period = self.max_times[-1] - self.zero_times[-1]
            self.quarter_periods.append(quarter_period)


        ### Moving robot:
        
        if self.quarter_periods:
            fold = values['time'] + TOLERANCE >= self.max_times[-1] + self.quarter_periods[-1]
            unfold = values['time'] + TOLERANCE >= self.zero_times[-1] + self.quarter_periods[-1]
            
            if fold and self.position != "folded":
                self.set_posture("folded")
            
          
            elif unfold and self.position != "unfolded":
                self.set_posture("unfolded")