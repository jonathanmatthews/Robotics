import numpy as np
from numpy import sign

class Increase():

    def __init__(self, values, all_data, **kwargs):
        """
        Set up the parameters for parametric pumping.
        """
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', float("inf"))
        
        self.prev, self.curr = 0.0, values['be']
        self.prev_time, self.curr_time = 0.0, values['time']
        self.moving_down = True
        
        self.max_times = self.last_maxima(all_data)
        self.min_times = self.last_minima(all_data)
        
        self.time_to_switch_unfolded = 100
        self.time_to_switch_folded =100
        
    
    def last_maxima(self, all_data):
        """
        Obtain the time of the last maxima, on either side of the swing.
        """
        be = np.abs(all_data['be'][-30:])
        time = all_data['time'][-30:]
        
        angle_max_index = (np.diff(np.sign(np.diff(be))) < 0).nonzero()[0] + 1 # Obtain index.
        max_times = time[angle_max_index]

        return max_times
        
    
    def last_minima(self, all_data):
        """
        Obtain the time at which the swing was last at the bottom of its arc.
        """
        be = np.abs(all_data['be'][-30:])
        time = all_data['time'][-30:]
        
        angle_max_index = (np.diff(np.sign(np.diff(be))) > 0).nonzero()[0] + 1 # Obtain index.
        min_times = time[angle_max_index]

        return min_times

    
    def algo(self, values, all_data, **kwargs):
        """
        Define parametric swinging function, for current swing state 'values' and past states 'all_data'.
        See interface.py for details.
        """

        TOLERANCE = 0.4 # How many seconds early the robot is allowed to switch positions.

        if values['av'] > 0 and not self.moving_down:
            # The robot seems to change a bit too early more frequently at the positive extreme,
            # so decrease tolerance in this case by a small amount.
            TOLERANCE += -0.2

        ### Getting period:

        # Shuffle values around, such that we compare the current state to
        # the previous state.

        self.prev, self.curr = self.curr, values['be']
        self.prev_time, self.curr_time = self.curr_time, values['time']
        
        if sign(self.curr) != sign(self.prev): # Zero crossed
            print values['time'], 'Crossed zero point'
            self.moving_down = False
            self.max_times = self.last_maxima(all_data)
            quarter_period = abs(self.max_times[-1] - values['time'])
            self.time_to_switch_unfolded = values['time'] + quarter_period
        
        elif abs(self.curr) <= abs(self.prev) and not self.moving_down: # Top of swing reached.
            print values['time'], 'At maximum'
            self.moving_down = True
            # Moving down flag prevents max_times from being appended to more than once.

            self.zero_times = self.last_minima(all_data)
            quarter_period = abs(values['time'] - self.zero_times[-1])
            self.time_to_switch_folded = values['time'] + quarter_period     
        
        if values['time'] + TOLERANCE > self.time_to_switch_unfolded:
            self.time_to_switch_unfolded += 100 # Some arbitrary big number.

            return 'unfolded' # Change position.
            
        if values['time'] + TOLERANCE > self.time_to_switch_folded:
            self.time_to_switch_folded += 100 # Some arbitrary big number.

            return 'folded' # Change position.
