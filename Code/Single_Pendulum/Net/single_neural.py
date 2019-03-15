import network_python2


class Neural():

    def __init__(self, values, all_data, **kwargs):
        self.net = network_python2.Net()

        self.angles_vertical = {
            'seated': -1.0461461544036865,
            'extended': -0.49697399139404297
        }
        self.difference = abs(self.angles_vertical['seated'] - self.angles_vertical['extended'])
        self.seated_angle = 0.0
        self.extended_angle = self.seated_angle - self.difference
        print self.seated_angle, self.extended_angle
        self.final_angles = {
            'seated': self.seated_angle,
            'extended': self.extended_angle
        }

        self.start_time = values['time']
        self.duration = kwargs.get('duration', float('inf'))

    def algo(self, values, all_data):
        print 'Machine Learning', values['time'], values['be']

        body_pos = values['pos']
        vertical_angle = self.final_angles[body_pos]

        forward, backward = self.net.output([values['be'], values['av'], vertical_angle])

        if forward >= backward:
            return 'seated'
        else:
            return 'extended'
        
        if values['time'] - self.start_time > self.duration:
            return 'switch'
