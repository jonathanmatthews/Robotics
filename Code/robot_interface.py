# python2.7
"""
Author: Jonathan Matthews.

A modules containing a class with which to access data about the robot and control it.

Contains class:
  Robot

Requires:
  naoqi
  hingeencoder
  encoder_functions
"""

from sys import path
from datanames import values
from time import time, sleep, gmtime, strftime
from utility_functions import flatten

try:
  path.insert(0, "hidlibs") # Insert encoder path.
  from pynaoqi.naoqi import ALProxy
  import top_encoder.encoder_functions as BigEncoder
  import bottom_encoder.hingeencoder as LittleEncoders
  encoders_available = True
  print "Modules loaded successfully"
  
except Exception as e:
    training = True
    print "Exception", e
    print "Error: unable to load encoder functions, encoder data will be unavailable"
    encoders_available = False
    if training:
        path.insert(0, "Training_functions")
        import BigEncoder
        import LittleEncoders
        from naoqi import ALProxy
        encoders_available = True



class Robot():
    """
    Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
    """
  
    def __init__(self, ip="192.168.1.3", port=9559, initial_position="Stand"):
        """
        Sets up the connection to the robot and sets initial posture. Also calibrates encoders to zero, if available.
        Requires arguments:

        ip : string, contains the IPv4 address of the robot to connect to.
        port : int, contains the port number through which to access the robot.
        """

        # Set up connection manager.
        #self.connection = ALProxy("ALConnectionManager", ip, port)
        #print("Network state: " + self.connection.state())

        self.speech = ALProxy("ALTextToSpeech", ip, port)
        self.speech.say("Connected")

        # Set up proxies to robot.
        #self.motion = ALProxy("ALMotion", ip, port)
        #self.posture = ALProxy("ALRobotPosture", ip, port)
        self.memory = ALProxy("ALMemory", ip, port)


        # Set up encoders, if available.
        if encoders_available:
            LittleEncoders.calibrate()
            BigEncoder.calibrate()


        #self.posture.goToPosture(initial_position, 1.0) # Set initial position.

    def get_gyro(self):
        """
        Obtain the current gyroscope data. Returns a tuple containing the (x, y, z) gyroscope data,
        in rad/s.
        """

        x_data = self.memory.getData(values['GX'][1])
        y_data = self.memory.getData(values['GY'][1])
        z_data = self.memory.getData(values['GZ'][1])

        return [x_data, y_data, z_data]

    def get_acc(self):
        """
        Obtain the current accelerometer data. Returns a tuple containing the (x, y, z) acceleromenter data,
        in m/s.
        """
        x_data = self.memory.getData(values['AX'][1])
        y_data = self.memory.getData(values['AY'][1])
        z_data = self.memory.getData(values['AZ'][1])

        return [x_data, y_data, z_data]

    @staticmethod
    def get_little_encoders():
        """
        Return the angles recorded by the small hinge encoders, at the base of the sqing, at the time of calling.
        If encoders are not available, will return None *without* producing an error.
        Returns a tuple, where the index of each value is the same as numbered in the source file from previous years.
        """

        if encoders_available:
            encoder0 = LittleEncoders.getAngle0()
            encoder1 = LittleEncoders.getAngle1()
            encoder2 = LittleEncoders.getAngle2()
            encoder3 = LittleEncoders.getAngle3()
            
            return [encoder0, encoder1, encoder2, encoder3]

    @staticmethod
    def get_big_encoder():
        """
        Returns the numerical value read from the large encoder at the top of the swing, if available. Else returns None,
        *without* producing an error.
        """

        if encoders_available:
            return BigEncoder.getAngle()

    @staticmethod
    def store(f, values):
        """
        Stores list of values
        f: reference to file (with open() as f)
        values: list of values to store
        """

        values = [str(x) for x in values]
        f.write(", ".join(values) + "\n")
        return

    @staticmethod
    def algorithm(time, acc, gyro, l_encoder, b_encoder):
        print time, acc, gyro, l_encoder, b_encoder


    def run(self, t, period):
        """
        t: time to run for
        period: period of cycle time
        """
        max_runs = t * 1/period
        file_name = strftime("%d-%m-%Y %H:%M:%S", gmtime())

        with open('Output_data/'+file_name, 'w') as f:
            counter = 0
            while counter < max_runs:
                start_time = time()

                # needs to be list of lists for easy flattening for storage while retaining ease of use for 
                # putting into algorithm
                values = [start_time, self.get_acc(), self.get_gyro(), self.get_little_encoders(), self.get_big_encoder()]
                self.algorithm(*values)
                
                flat_values = flatten(values)
                self.store(f, flat_values)

                counter += 1

                cycle_time = time() - start_time
                if cycle_time < period:
                    sleep(period - cycle_time)
                    
            f.close()
        if  cycle_time > period:
            print('Ran behind schedule')
        else:
            print('Ran on time')
        print('Stored {:.0f} lines in {}'.format(max_runs, file_name))
      
robot = Robot()
robot.run(5, 0.1)
      
  
  
  
  
  
  
  
  
