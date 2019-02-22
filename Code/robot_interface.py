# python2.7
"""
A modules containing a class with which to access data about the robot and control it.

Contains class:
  Robot
"""


class Robot():
    """
    Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
    """

    def __init__(self, values, positions, ALProxy,
                 ip="192.168.1.3", port=9559):
        """
        Sets up the connection to the robot and sets initial posture. Also calibrates encoders to zero, if available.
        Requires arguments:

        values: dictionary containing information of robot limb data
        positions: dictionary containing different preset positions
        ip : string, contains the IPv4 address of the robot to connect to.
        port : int, contains the port number through which to access the robot.
        """
        # Store for later
        self.values = values
        self.positions = positions

        # Set up connection
        self.speech = ALProxy("ALTextToSpeech", ip, port)
        self.speech.say("Connected")

        # Set up proxies to robot
        self.motion = ALProxy("ALMotion", ip, port)
        self.memory = ALProxy("ALMemory", ip, port)

        # Not as easy to store text in numpy so numbers correspond to positions
        # THIS WILL BE CHANGED IT IS A TEMPORARY FIX I KNOW IT'S A PAIN
        self.position_names = {
            'extended': 1,
            'seated': 0,
            'initial_seated': -1,
            1: 'extended',
            0: 'seated',
            -1: 'initial_seated'
        }
        self.position = 'seated'

    def get_gyro(self):
        """
        Obtain the current gyroscope data. Returns a tuple containing the (x, y, z) gyroscope data,
        in rad/s.
        """
        x_data = self.memory.getData(self.values['GX'][1])
        y_data = self.memory.getData(self.values['GY'][1])
        z_data = self.memory.getData(self.values['GZ'][1])

        return [x_data, y_data, z_data]

    def get_acc(self):
        """
        Obtain the current accelerometer data. Returns a list containing the (x, y, z) acceleromenter data,
        in m/s.
        """
        x_data = self.memory.getData(self.values['ACX'][1])
        y_data = self.memory.getData(self.values['ACY'][1])
        z_data = self.memory.getData(self.values['ACZ'][1])

        return [x_data, y_data, z_data]

    def get_angle(self, part_name):
        """
        Get the current angle of the named part.
        Requires:
        part_name : the name of the part as written in the values dictionary.
        Example:
        angle, name = self.get_angle('HY')
        """
        limb_info = self.values[part_name]
        angle = self.memory.getData(limb_info[1])
        name = limb_info[0]
        return angle, name

    def set_posture(self, name_posture, max_speed=1.0):
        """
        Sets the robot's posture. Posture should be described with a name corresponding to a dictionary.
        Requires:
        name_posture : name, corresponds to dictionary in positions.py.
        max_speed : float, optional. The speed to move at. Default 1.0.
        Examples:
        set_posture('extended')
        set_posture('seated')
        """
        # Extract dictionary corresponding to name_posture
        posture = self.positions[name_posture]
        # Use names in dictionary to collect longer name that naoqi uses
        names = [self.values[name][0] for name in posture.keys()]
        # Create list of speeds such that movements finish at same time
        speed = [max_speed * (self.values[named_part_range][5] / 1.4920799999999999) for named_part_range in posture.keys()]
        #speed = [max_speed * (self.values[named_part_range][4]/self.values['HY'][4]) for named_part_range in posture.keys()]
        # Need stiffness set to 1.0 before can move
        self.motion.setStiffnesses(
            ["Head", "RArm", "LArm", "RLeg", "LLeg"], 1)
        # Start movement of each part
        for i in range(len(speed)):
            self.motion.setAngles(
                names[i], list(
                    posture.values())[i], speed[i])
        # Update current position
        self.position = name_posture
