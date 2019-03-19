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
from single_decrease_small_angle import DecreaseSmallAngle
from single_increase_max_angle import IncreaseMaxAngle
from single_stopping_variable_speed import StoppingVariableSpeed
from triple_increase_angular_velocity import TripleIncreaseAngularVelocity


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
            'duration': 5
        },{
            'algo': DecreaseSmallAngle,
            'duration': 60
        }]

        #self.order = [{
            #'algo': Nothing,
            #'duration': 10
        #},{
            #'algo': MaintainFeedback,
            #'duration': 90,
            #'masses': True
        #}]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 90
        #}]

        #self.order = [{
            #'algo': Nothing,
            #'duration': 10
        #},

        #self.order = [{
            #'algo': Start,
            #'duration': 25
        #},{
            #'algo': IncreaseQuarterPeriod,
            #'max_angle': 15
        #},
            ##'algo': DecreaseQuarterPeriod,
            ##'increasing': False,
            ##'min_angle': 10
        ##},{
            ##'algo': MaintainConstant,
            ##'duration': 45
        #{
            #'algo': IncreaseParametric,
            #'duration': 60,
            #'max_angle': 40
        #},{
            #'algo': DecreaseParametric,
            #'duration': 60,
            #'increasing': False,
            #'min_angle': 5
        #},{
            #'algo': Nothing,
            #'duration': 10
        #}]

        for dictionary in self.order:
            dictionary['period'] = period
