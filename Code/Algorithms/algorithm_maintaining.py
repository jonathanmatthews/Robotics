from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
from single_nothing import Nothing
from single_maintain_improved import MaintainGoodBadKick


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
            'duration': 10.0
        },{
            'algo': MaintainGoodBadKick,
            'maintain_angle': 7.5
        }]



        for dictionary in self.order:
            dictionary['period'] = period
