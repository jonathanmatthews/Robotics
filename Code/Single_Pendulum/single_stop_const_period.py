'''Stop algorithm that simply kicks, waits a half period,
    and kicks again. Calculates correct kicking order as will already be in 
    motion, and times starting kick to next maxima.'''


from utility_functions import last_maxima

class Stop():
    def __init__(self, values, all_data, **kwargs):
        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))
        self.min_angle = kwargs.get('min_angle', 1.0)
        self.wait_time = 1.4
        self.last_move = last_maxima(all_data, 'time')
        self.offset = -0.3

        # sets up correct position
        av = values['av']
        if av >= 0:
            # positive angular momentum means going backward, therefore want seated to decrease
            self.next_pos = 'seated'
        else:
            # opposite of above
            self.next_pos = 'extended'
        print 'Stopping swing, constant period'

    def algo(self, values, all_data):
        t = values['time']

        if t > self.last_move + self.wait_time + self.offset:
            print 'Last maxima {}'.format(abs(last_maxima(all_data, 'be')))
            print 'Stop swing', values['time']
            self.last_move = t
            return self.next_position()

        # ending if duration is over or minimum angle is reached
        if t - self.start_time > self.duration:
            print 'duration reached, stopping'
            return 'switch'
        if abs(last_maxima(all_data, 'be')) < self.min_angle:
            print 'min angle reached, stopping'
            return 'switch'

    def next_position(self):
        if self.next_pos == 'seated':
            self.next_pos = 'extended'
            return 'seated'
        else:
            self.next_pos = 'seated'
            return 'extended'
