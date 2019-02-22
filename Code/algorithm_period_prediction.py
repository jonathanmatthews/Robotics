from robot_interface import Robot
from encoder_interface import Encoders
import math


class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy)

        # Run code for set up of algorithm here e.g.
        self.speech.say("Setting up algorithm")
        self.set_posture("seated")
        self.max_angle = 0
        self.record_start = None
        self.recording_mode = True
        self.next_kick_turn = None
        self.period = None
        self.change_pos_time = 0.5
        self.algorithm = self.algorithm_start
        self.first_kick = True

    def algorithm_start(self,values):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        time = values['time']
        b_encoder = values['be']
        # this switches algorithm after time is greater than 10
        print(b_encoder)
        if time > 10 and b_encoder<0.5 and b_encoder>-0.5:
            print("switching algorithm")
            self.algorithm = self.algorithm_increase
        else:
            pass

    def algorithm_increase(self, values):
        pos = values['position']
        angular_v = values['av']
        t = values['event']
        b_encoder = values['be']
        print(12235)
        #check if the robot start to kick for the first time, for the first kick, we check the angular velocity
        #for different postures to change the posture
        if(self.first_kick == True):
            self.first_kick = False
            if(pos == 'extended' and angular_v >= 0):
                #The t here means the turn not the time!!!
                self.set_posture("seated")
                self.record_start = t
            elif(pos == 'extended' and angular_v <= 0):
                self.set_posture("extended")
                self.record_start = t
        else:
            if(self.recording_mode ==False):
            
                if(t == self.next_kick_turn):
                    
                    self.recording_mode = True
                    if(pos  == 'extended'):
                        self.set_posture('seated')
                    else:
                        self.set_posture('extended')
            
            elif(b_encoder<0.5 and b_encoder>-0.5 and self.recording_mode == True):
                
                recording_mode = False
                self.period = t - self.record_start
                self.next_kick_turn = t + self.period-math.ceil(self.change_pos_time/0.1)
                self.record_start = t+self.period
                print(r'{t} + {self.period}')