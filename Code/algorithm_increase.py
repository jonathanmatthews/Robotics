from time import time

class IncreaseDecrease():

    def __init__(self, values, all_data, **kwargs):
        self.start_time = time()
        self.max_angle = kwargs.get('max_angle', 20)
        self.increase = kwargs.get('increase', True)
        self.duration = kwargs.get('duration', 20)


    def algo(self, values, all_data):
        if self.increase:
            print 'Increase', values['time']
            if values['be'] > self.max_angle:
                return 'switch'
        else:
            print 'Decrease', values['time']
        if time() - self.start_time > self.duration:
            return 'switch'