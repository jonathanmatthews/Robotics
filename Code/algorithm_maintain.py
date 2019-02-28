from time import time

class Maintain():

    def __init__(self, values):
        self.start_time = time()

    def algo(self, values, **kwargs):
        maintain_angle = kwargs.get('maintain_angle', 10)
        duration = kwargs.get('duration', 15)
        print 'Maintain', values['time']

        if time() - self.start_time > duration:
            return 'switch'