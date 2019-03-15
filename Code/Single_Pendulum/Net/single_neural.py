import network_python2


class Neural():

    def __init__(self, values, all_data, **kwargs):
        self.net = network_python2.Net()
        self.last_switch_time = values['time']

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
        print 'Machine Learning', values['time'], values['be'], values['pos']

        body_pos = values['pos']
        vertical_angle = self.final_angles[body_pos]

        forward, backward = self.net.output([values['be'], values['av'], vertical_angle])
        
        if values['time'] < 30:
            if values['time'] - 1.1 > self.last_switch_time:
                if forward >= backward and values['pos'] == 'extended':
                    self.last_switch_time = values['time']
                    return 'seated'
                elif backward > forward and values['pos'] == 'seated':
                    self.last_switch_time = values['time']
                    return 'extended'
                else:
                    print 'Other condition', forward, backward, values['time'], self.last_switch_time
        else:
            if values['time'] - 0.5 > self.last_switch_time:
                if forward >= backward and values['pos'] != 'seated':
                    return 'seated'
                elif backward > forward and values['pos'] != 'extended':
                    return 'extended'
                
        #if forward >= backward and values['pos'] != 'seated':
            #return 'seated'
        #elif backward > forward and values['pos'] != 'extended':
            #return 'extended'
        
        if values['time'] - self.start_time > self.duration:
            return 'switch'
