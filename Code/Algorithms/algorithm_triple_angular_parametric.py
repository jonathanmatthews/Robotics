from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
path.insert(0, 'Triple_Pendulum')

from triple_startup_const_period import Start
from triple_increase_angular_velocity_parametric_2 import TripleIncreaseAngularVelocity



class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders, angvel_avg=1)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [{
            'algo': Start,
            'duration': 5
        },{
            'algo': TripleIncreaseAngularVelocity 
        }]


        for dictionary in self.order:
            dictionary['period'] = period
