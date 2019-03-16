from utility_functions import sign_zero, total_angle

class TripleIncreaseAngularVelocity():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.increasing = kwargs.get('increasing', True)
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 5)
        self.previous_max_angle = total_angle(all_data['be'], all_data['se0'], all_data['se1']).max()
        self.previous_be = total_angle(values['be'], values['se0'], values['se1'])
    

    def algo(self, values, all_data):
        """
        Use the angular velosity to estimate the time to switch the posture
        """
        self.current_be = total_angle(values['be'], values['se0'], values['se1'])
        print 'Time: {:.2f}'.format(values['time']), 'Total angle value: {:.2f}'.format(self.current_be)
        
        print sign_zero(self.previous_be), sign_zero(self.current_be)
        if(sign_zero(self.previous_be)==-1 and self.previous_be - self.current_be <0):
            self.previous_be = self.current_be
            if(self.increasing == True):
                return ['seated', 0.4]
            elif(self.increasing == False):
                return ['extended', 0.4]
            self.previous_max_angle = self.previous_be
            print('max_angle', self.previous_be)
        elif(sign_zero(self.previous_be)==1 and self.previous_be - self.current_be >0):
            self.previous_be = self.current_be
            if(self.increasing == True):
                return ['extended', 0.4]
            elif(self.increasing == False):
                return ['seated', 0.4]
            self.previous_max_angle = self.previous_be
            print('max_angle', self.previous_be)
            
        self.previous_be = self.current_be
        
        # switch conditions
        if(self.increasing == True):
            if abs(self.current_be) > self.max_angle:
                return 'switch'
        elif(self.increasing == False):
            print 'Decrease', values['time']
            if abs(self.previous_max_angle) < self.min_angle:
                return 'switch'
        if values['time'] - self.start_time > self.duration:
            return 'switch'
        
class TripleDecreaseAngularVelocity(TripleIncreaseAngularVelocity):
    def __init__(self, values, all_data, **kwargs):
        TripleIncreaseAngularVelocity.__init__(self, values, all_data, **kwargs)
 
