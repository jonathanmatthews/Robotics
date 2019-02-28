from time import time

class IncreaseDecrease():

    def __init__(self, values):
        self.start_time = time()

    def algo(self, values, **kwargs):
        max_angle = kwargs.get('max_angle', 20)
        increase = kwargs.get('increase', True)
        duration = kwargs.get('duration', 20)

        if increase:
            print 'Increase', values['time']
            if values['be'] > max_angle:
                return 'switch'
        else:
            print 'Decrease', values['time']
        if time() - self.start_time > duration:
            return 'switch'