from time import time

class Start():
    def __init__(self, values, **kwargs):
        self.start_time = time()
        self.duration = kwargs.get('duration', 10)
        self.wait_time = 1.3
        self.last_move = 0
        self.set_posture('extended')
        pass
    
    def algo(self, values):
        print 'start', values['time']
        t = values['time']
        if t > self.last_move + self.wait_time:
            self.last_move = t
            if self.position == 'extended':
                self.set_posture('seated')
            else:
                self.set_posture('extended')

        if time() - self.start_time > self.duration:
            return 'switch'