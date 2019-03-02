from robot_interface import Robot
from encoder_interface import Encoders
from single_startup_const_period import Start
from single_increase_quarter_period import IncreaseQuarterPeriod
from single_nothing import Nothing

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
        self.increase= IncreaseQuarterPeriod
        self.decrease = IncreaseQuarterPeriod
        self.start = Start

        # This defines the order of running, and any extra arguments required for the functions
        # are defined in the dictionary
        # This algorithm runs the startup algorithm for 2 seconds, then runs increase till it reaches
        # 20 degrees or for 3 seconds, then maintains at 20 degrees for 2 seconds, and then finally
        # decreases for 20 seconds or the end of the running time
        self.order = [{
            'algo': self.start,
            'duration': 2.0
        },{
            'algo': self.increase,
            'max_angle': 30.0,
            'duration': 3.0
        }]
        
