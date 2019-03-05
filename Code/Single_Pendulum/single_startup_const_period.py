'''Start-up algorithm that simply kicks, waits a half period,
    and kicks again.'''

class Start():
    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', 10)
        self.wait_time = 1.25   # defined by the half period of a swing
        self.last_move = 0      # time last kick was performed
        self.first_kick = True  # used to check if it is first kick
        pass
    
    def algo(self, values, all_data):
        print 'start', values['time']
        t = values['time']  # renames current time to t

        if t < 0.1:
            # sets the first kick from standstill. 
            self.last_move = t  # resets time of last kick
            return 'extended'   # kicks
        
        
        if t > 0.1:
            if t > self.last_move + self.wait_time/2 and self.first_kick == True:
                # first kick needed after a quarter period, not half
                self.first_kick = False  # go to half period kicks
                self.last_move = t       # reset time of last kick
                if values['pos'] == 'seated':
                    return 'extended'
                else:
                    return 'seated'

            if t > self.last_move + self.wait_time:
                # kicks after first kick use quarter period
                self.last_move = t  # reset time of last kick
                if values['pos'] == 'extended':
                    return 'seated'
                else:
                    return 'extended'

        
        if t - self.start_time > self.duration and 0.15 < t - self.last_move < 0.5:
            print 'last move', self.last_move
            return 'switch'
