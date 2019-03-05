from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
from single_startup_const_period import Start
from single_nothing import Nothing
from single_increase_quarter_period import IncreaseQuarterPeriod

class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=False)

        self.order = [{
            'algo': Start,
            'duration': 10.0
        },{
            'algo': IncreaseQuarterPeriod,
            'duration': 20.0
        }]
        
