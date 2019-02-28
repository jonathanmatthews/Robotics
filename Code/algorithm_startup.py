from time import time

class Start():
    def __init__(self, values):
        self.start_time = time()
        pass
    
    def algo(self, values, **kwargs):
        duration = kwargs.get('duration', 5)
        print 'start', values['time']
        if time() - self.start_time > duration:
            return 'switch'