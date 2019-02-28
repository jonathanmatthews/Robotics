from time import time

class Start():
    def __init__(self, values, **kwargs):
        self.start_time = time()
        self.duration = kwargs.get('duration', 10)
        self.wait_time = 1.3
        self.last_move = 0
        pass
    
    def algo(self, values):
        print 'start', values['time']
        t = values['time']
        if t < 0.1:
            self.last_move = t
            return 'extended'
        
        if t > 0.1:
            if t > self.last_move + self.wait_time:
                self.last_move = t
                if values['pos'] == 'extended':
                    return 'seated'
                else:
                    return 'extended'

        if time() - self.start_time > self.duration:
            return 'switch'