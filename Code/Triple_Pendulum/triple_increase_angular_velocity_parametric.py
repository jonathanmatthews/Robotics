from utility_functions import sign_zero, total_angle
from time import sleep

class TripleIncreaseAngularVelocity():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increasing = kwargs.get('increasing', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 5)
        self.previous_max_angle = total_angle(all_data['be'], all_data['se0'], all_data['se1']).max()
        self.previous_be = total_angle(values['be'], values['se0'], values['se1'])
        self.previous_av = values["av"]
    

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        self.current_be = total_angle(values['be'], values['se0'], values['se1'])
        self.current_av = values["av"]
        print 'Time: {:.2f}'.format(values['time']), 'Total angle value: {:.2f}'.format(self.current_be)
        
        if abs(self.previous_be) > abs(self.current_be): # Hit a maxima.
	    if self.increasing:
	        return ["lowered", 0.5] # This speed should be tested on the robot.
	    
	    else:
	        return ["raised", 0.5]
	
	    self.previous_max_angle = self.previous_be
	    print("max_angle", self.previous_be)
	
        elif abs(self.previous_av) > abs(self.current_av): # Hit a zero.
	    if self.increasing:
	        return ["raised", 0.5]
	    
	    else:
	        return ["lowered", 0.5]
        
        self.previous_be = self.current_be
        self.previous_av = self.current_av
        
        # switch conditions
        if self.increasing:
            if abs(self.current_be) > self.max_angle:
                return 'switch'
	      
        else:
            print 'Decrease', values['time']
            
            if abs(self.previous_max_angle) < self.min_angle:
                return 'switch'
	      
        if values['time'] - self.start_time > self.duration:
            return 'switch'
        
class TripleDecreaseAngularVelocity(TripleIncreaseAngularVelocity):
    def __init__(self, values, all_data, **kwargs):
        TripleIncreaseAngularVelocity.__init__(self, values, all_data, **kwargs)
 
