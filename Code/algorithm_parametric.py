from robot_interface import Robot
from encoder_interface import Encoders
from parametric_increase import Increase
from single_startup_const_period import Start
from single_increase_quarter_period import IncreaseQuarterPeriod


class Algorithm(Robot, Encoders):
    """
    This is an example algorithm class, as everyone will be working on different algorithms
    """

    def __init__(self, BigEncoder, SmallEncoders, values, positions, ALProxy):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy)

        # These are the classes that all containing the function algorithm that will be run,
        # this classes will be initialised one cycle before switching to the algorithm
        self.increase1 = IncreaseQuarterPeriod
        self.increase2 = Increase
        self.start = Start
        
        self.order = [{
            'algo': self.start,
            'duration': 30.0
        },{
            'algo': self.increase1,
            'max_angle': 10
        },{
            'algo': self.increase2
        }]
