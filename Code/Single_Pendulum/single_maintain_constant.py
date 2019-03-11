from numpy import sign
from utility_functions import last_maxima
"""
This algorithm is garbage, it still gains amplitude when run, worth talking about
flaw in the report, isn't adaptive.
"""

class MaintainConstant():
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, values, all_data, **kwargs):
        print 'Starting maintain'
        self.start_time = values['time']
        self.max_angle = kwargs.get('max_angle', 180)
        self.maintain_angle = kwargs.get('maintain_angle', 10)
        self.duration = kwargs.get('duration', 20)
        
        masses = kwargs.get('masses', True)
        if masses:
            self.offset_angle = 15
        else:
            self.offset_angle = 5

        self.previous_be = values['be']

    def algo(self, values, all_data):
                # sign of big encoder changes when crossing zero point
        if sign(values['be']) != sign(self.previous_be):
            self.max_angle = last_maxima(all_data, be_time='be')
            print 'Last maximum angle {}'.format(self.max_angle)

            # If angle of last swing is greater than the maintain angle then 
            # want to kick earlier to counteract it, vice versa for smaller
            if abs(self.max_angle) > self.maintain_angle + 0.5:
                self.offset_angle += 0.5
                print '\033[1mChanging offset to {} degrees\033[0m'.format(self.offset_angle)
            if abs(self.max_angle) < self.maintain_angle - 0.5:
                self.offset_angle -= 0.5
                print '\033[1mChanging offset to {} degrees\033[0m'.format(self.offset_angle)

        self.previous_be = values['be']

        if values['be'] > self.maintain_angle - self.offset_angle and values['pos'] != 'extended' and values['av'] > 0:
            print values['pos']
            print 'Should kick at greater than {}, actually kicking at {}'.format(self.maintain_angle - self.offset_angle, values['be'])
            return 'extended'
        if values['be'] < -self.maintain_angle + self.offset_angle and values['pos'] != 'seated' and values['av'] < 0:
            print values['pos']
            print 'Should kick at less than {}, actually kicking at {}'.format(-self.maintain_angle + self.offset_angle, values['be'])
            return 'seated'

        if values['time'] - self.start_time > self.duration:
            print '\033[1mDuration over, switching algorithm\033[0m'
            return 'switch'
