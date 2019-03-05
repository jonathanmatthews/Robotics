from single_increase_parametric_rework import Increase
from single_maintain_constant import MaintainConstant
from single_stop_const_period import Stop
from single_nothing import Nothing
from single_increase_max_angle_damping import IncreaseDecrease
from single_startup_const_period import Start
from robot_interface import Robot
from encoder_interface import Encoders

from sys import path
path.insert(0, 'Single_Pendulum')


class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy, masses=False)

        # These are the classes that all containing the function algorithm that will be run,
        # this classes will be initialised one cycle before switching to the algorithm

        self.increase = IncreaseDecrease
        self.increase_parametric = Increase
        self.start = Start
        self.stop = Stop
        self.maintain = MaintainConstant
        self.nothing = Nothing

        # This defines the order of running, and any extra arguments required for the functions
        # are defined in the dictionary
        self.order = [{
            'algo': self.nothing,
            'duration': 5.0
        }, {
            'algo': self.increase_parametric,
            'duration': 300
        }]

        # self.order = [{
        # 'algo': self.start,
        # 'duration': 25.0
        # },{
        # 'algo': self.increase,
        # 'max_angle': 15.0,
        # 'min_angle': 5.0,
        # 'Increase' : True,
        # 'duration': 50.0
        # },{
        # 'algo': self.maintain,
        # 'max_angle': 15.0,
        # 'duration': 60.0
        # },{
        # 'algo': self.increase_parametric,
        # 'duration': 50.0,
        # 'max_angle': 20.0
        # },{
        # 'algo': self.stop,
        # 'min_angle': 1,
        # 'duration': 100
        # },{
        # 'algo': self.nothing
        # }]
