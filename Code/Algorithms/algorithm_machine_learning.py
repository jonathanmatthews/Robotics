from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
from single_nothing import Nothing
path.insert(0, 'Single_Pendulum/Net')
from single_neural import Neural

class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [{
            'algo': Nothing,
            'duration': 3
        },{
            'algo': Neural,
        }]

        for dictionary in self.order:
            dictionary['period'] = period
