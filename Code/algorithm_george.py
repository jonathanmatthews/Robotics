from robot_interface import Robot
from encoder_interface import Encoders
from single_increase_angular_velocity import IncreaseDecrease
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
        self.increase = IncreaseDecrease
        self.start = Nothing

        # This defines the order of running, and any extra arguments required for the functions
        # are defined in the dictionary
        # This algorithm runs the startup algorithm for 2 seconds, then runs increase till it reaches
        # 20 degrees or for 3 seconds, then maintains at 20 degrees for 2 seconds, and then finally
        # decreases for 20 seconds or the end of the running time
        self.order = [{
            'algo': self.start
        },
        {
            'algo': self.increase,
            'max_angle': 20,
            'duration': 10
        }]
        
