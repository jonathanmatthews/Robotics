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
from triple_increase_james import TripleIncreaseQuarterPeriod
from single_decrease_low_angle import DecreaseSmallAngle
from single_increase_max_angle import IncreaseMaxAngle
from single_maintain_improved import MaintainGoodBadKick

class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy, period):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders, small_encoders_required=False)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=False, acc_required=False, gyro_required=False)

        self.order = [{
            'algo': Nothing,
            'duration': 20
        },{        
            'algo': Start,
            'duration': 30
        },{
            'algo': IncreaseQuarterPeriod,
            'increasing': True,
            'max_angle': 5.0
        },{
            'algo': MaintainGoodBadKick,
            'maintain_angle': 5,
            'duration': 60
        },{
            'algo': IncreaseQuarterPeriod,
            'max_angle': 7.5
        },{
            'algo': MaintainGoodBadKick,
            'maintain_angle': 7.5,
            'duration': 60
        },{
            'algo': IncreaseQuarterPeriod,
            'min_angle': 5,
            'increasing': False
        },{
            'algo': MaintainGoodBadKick,
            'duration': 230,
            'maintain_angle': 5

        }]
        
        #self.order = [{
            #'algo': Nothing,
            #'duration': 10
        #},{
            #'algo': MaintainFeedback,
            #'maintain_angle': 7.5
        #}]

        for dictionary in self.order:
            dictionary['period'] = period
