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
        self.already_passed_zero = False
        self.already_passed_maxima = False
    

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        self.current_be = total_angle(values['be'], values['se0'], values['se1'])
        self.current_av = values["av"]
        print 'Time: {:.2f}'.format(values['time']), 'Total angle value: {:.2f}'.format(self.current_be)
        
        if abs(self.current_av) <= abs(self.previous_av) and not self.already_passed_zero:
        #if sign_zero(self.current_av) != sign_zero(self.previous_av) and not self.already_passed_zero:
            #print("AVs:", self.previous_av, self.current_av, "time:", values['time'], "raise")
            self.previous_be = self.current_be
            self.previous_av = self.current_av
            self.already_passed_zero = True # Already past minima, don't send the signal again.
            self.already_passed_maxima = False

            if self.increasing:
                print "raise"
                return ["raised", 0.5]
            else:
                return ["lowered", 0.5]

        if abs(self.previous_be) >= abs(self.current_be) and not self.already_passed_maxima:
            #print("BEs:", self.previous_be, self.current_be, "time", values['time'], "lower")
            self.already_passed_zero = False # Moving back down.
            self.already_passed_maxima = True
            self.previous_be = self.current_be
            self.previous_av = self.current_av
            
            
            self.previous_max_angle = self.previous_be
            print('max_angle', self.previous_be)
            
            if self.increasing:
                print "lower"
                return ['lowered', 0.5]
            else:
                return ['raised', 0.5]
            
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
 
