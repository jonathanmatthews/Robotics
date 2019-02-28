from time import time

class Maintain():

    def __init__(self, values, **kwargs):
        self.start_time = time()
        self.maintain_angle = kwargs.get('maintain_angle', 10)
        self.duration = kwargs.get('duration', 15)

    def algo(self, values, **kwargs):
        print 'Maintain', values['time']

        if time() - self.start_time > self.duration:
            return 'switch'