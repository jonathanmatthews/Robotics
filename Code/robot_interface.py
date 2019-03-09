# python2.7
"""
A modules containing a class with which to access data about the robot and control it.

Contains class:
  Robot
"""
from time import sleep

class Robot():
    """
    Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
    """

    def __init__(self, values, positions, ALProxy,
                 ip="192.168.1.3", port=9559, **kwargs):
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

        # Set up proxies to robot
        self.speech = ALProxy("ALTextToSpeech", ip, port)
        self.motion = ALProxy("ALMotion", ip, port)
        self.memory = ALProxy("ALMemory", ip, port)
        self.masses = kwargs.get('masses', True)
        self.set_posture_initial('seated', max_speed = 0.1)
        self.motion.setFallManagerEnabled(False)
        
    def check_setup(self, position):
        position = self.positions[position]
        values = [self.get_angle(key)[0] for key in position.keys()]
        differences = [(key, value, abs(value - position[key])) for (key, value) in zip(position.keys(), values)]
        
        for trip in differences:
            if trip[2] > 0.1:
                raise ValueError("Position isn't setting correctly, failed first on {}.\nDifference from expected value: {}".format(*trip))

    def get_gyro(self):
        """
        Obtain the current gyroscope data. Returns a tuple containing the (x, y, z) gyroscope data,
        in rad/s.
        """
        x_data = self.memory.getData(self.values['GX'][1])
        y_data = self.memory.getData(self.values['GY'][1])
        z_data = self.memory.getData(self.values['GZ'][1])
        # not sure whether the below works on not, worth testing
        # x_data, y_data, z_data = self.memory.getData([self.values['GX'][1], self.values['GY'][1], self.values['GZ'][1]])

        return [x_data, y_data, z_data]

    def get_acc(self):
        """
        Obtain the current accelerometer data. Returns a list containing the (x, y, z) acceleromenter data,
        in m/s.
        """
        x_data = self.memory.getData(self.values['ACX'][1])
        y_data = self.memory.getData(self.values['ACY'][1])
        z_data = self.memory.getData(self.values['ACZ'][1])
        # same again, not sure if this works but would be good to save time
        # x_data, y_data, z_data = self.memory.getData([self.values['ACX'][1], self.values['ACY'][1], self.values['ACZ'][1]])

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
        
    def set_posture(self, next_posture, current_posture, max_speed=1.0):
        next_posture_dict = self.positions[next_posture]
        current_posture_dict = self.positions[current_posture]
        print next_posture_dict
        print current_posture_dict
        
        differences_in_angles = []
        for name in next_posture_dict.keys():
            difference = abs(next_posture_dict[name] - current_posture_dict[name])
            if difference == 0:
                differences_in_angles.append(0.01)
            else:
                differences_in_angles.append(difference)
        max_difference = max(differences_in_angles)
        speeds = [max_speed * difference / max_difference for difference in differences_in_angles]
            
        part_name = [self.values[name][0] for name in next_posture_dict.keys()]
        
        print 'Name', part_name
        print 'Next posture', next_posture_dict.values()
        for name, value, speed in zip(part_name, next_posture_dict.values(), speeds):
            self.motion.setAngles(name, value, speed)
        self.position = next_posture
        
    def set_posture_initial(self, next_posture='seated', max_speed=0.2):
        self.motion.setStiffnesses("Body", 1.0)
        
        startup_dict = {}
        for key in self.positions[next_posture].keys():
            startup_dict[key] = self.get_angle(key)[0]
        self.positions['startup'] = startup_dict
        
        self.set_posture(next_posture, 'startup', max_speed=0.2)
        
        
        
