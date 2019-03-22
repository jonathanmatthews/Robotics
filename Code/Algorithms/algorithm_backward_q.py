from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')
path.insert(0, 'Triple_Pendulum')
from single_nothing import Nothing
from single_startup_const_period import Start
from single_maintain_constant import MaintainConstant
from single_maintain_feedback import MaintainFeedback
from single_stop_const_period import Stop
from single_increase_quarter_period import DecreaseQuarterPeriod, IncreaseQuarterPeriod
from single_increase_parametric_rework import DecreaseParametric, IncreaseParametric
# from triple_increase_james import TripleIncreaseQuarterPeriod
from single_increase_max_angle import IncreaseMaxAngle
from single_stopping_variable_speed import StoppingVariableSpeed
from triple_increase_angular_velocity import TripleIncreaseAngularVelocity
from single_increase_angular_velocity import IncreaseAngularVelocity
from triple_startup_const_period import Start
from single_increase_accelerometer import IncreaseAccelerometer
from single_backward_q import BackwardQ


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
            'algo': BackwardQ
        }]

        for dictionary in self.order:
            dictionary['period'] = period
