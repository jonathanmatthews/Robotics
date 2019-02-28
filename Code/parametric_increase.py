
from time import time

class Increase():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = time()
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', 999999999) # A big number.


    def algo(self, values, all_data, **kwargs):
        """
        Define parametric swinging function, for current swing state 'values'.
        See interface.py for details.
        """

        TOLERANCE = 0 # How many seconds early the robot is allowed to switch positions.


        ### Getting period:

        try:
            # Shuffle values around, such that we compare the current state to
            # the previous state.

            self.prev, self.curr = self.curr, values['be']
            self.prev_time, self.curr_time = self.curr_time, values['time']
        
        except: # If this is the first time this function is run.
            self.prev, self.curr = 0.0, 0.0
            self.prev_time, self.curr_time = 0.0, 0.0

            self.max_times = [] # Times at which max amplitude reached.
            self.zero_times = [] # Times at which zero point was reached.
            self.quarter_periods = []
        
        if sign(self.curr) != sign(self.prev): # Zero crossed
            self.zero_times.append(values['time'])
            self.moving_down = False
        
        elif abs(self.curr) <= abs(self.prev) and not self.moving_down:
            self.max_times.append(values['time'])
            self.moving_down = True

            # Moving down flag prevents max_times from being appended to more than once.
            
            quarter_period = abs(self.max_times[-1] - self.zero_times[-1])
            self.quarter_periods.append(quarter_period)


        ### Moving robot:
        
        self.switch_condition = False
        
        if self.switch_condition:
	  return "switch"
        
        if self.quarter_periods:
            fold = (values['time'] + TOLERANCE >= self.max_times[-1] + 2*self.quarter_periods[-1])
            unfold = (values['time'] + TOLERANCE >= self.zero_times[-1] + 2*self.quarter_periods[-1])
            
            if fold and self.position != "folded":
                self.position = "folded"
                return "folded"
            
            elif unfold and self.position != "unfolded":
                self.position = "unfolded"
	        return "unfolded"
                