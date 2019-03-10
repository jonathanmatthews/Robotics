from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
from single_nothing import Nothing
from single_maintain_constant import MaintainConstant
from single_maintain_feedback import MaintainFeedback

class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=True)

        self.order = [{
            'algo': Nothing,
            'duration': 5
        },{
            'algo': MaintainFeedback,
            'maintain_angle': 10,
            'duration': 30
        }]