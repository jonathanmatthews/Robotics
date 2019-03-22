from sys import path
path.insert(0, 'Single_Pendulum')

from single_nothing import Nothing
from single_increase_quarter_period import IncreaseQuarterPeriod
from single_startup_const_period import Start
from single_increase_parametric_rework import IncreaseParametric
from robot_interface import Robot
from encoder_interface import Encoders

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
            'duration': 20
        }, {
            'algo': IncreaseQuarterPeriod,
            'max_angle': 8.0
        }, {
            'algo': IncreaseParametric
        }]
