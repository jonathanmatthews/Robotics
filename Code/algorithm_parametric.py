from robot_interface import Robot
from encoder_interface import Encoders
from parametric_increase import Increase


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
        self.increase = Increase
        
        self.order = [{
            
        },{
            'algo': self.increase
        }]
