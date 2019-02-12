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

# Begin additional imports from robotcontrol2...
import os
import sys
from change_stiffness import *
from positionvalues import extended, seated
# End additional imports form robotcontrol2.


from sys import path
from datanames import values
import time as tme
from utility_functions import flatten
from shlex import split
from pandas import DataFrame, read_csv

###
### Set mode to run here
### Developing for running through real code away from encoders
### Testing for seeing how algorithm reacts to old dataset
### Real for in lab running from lab PC
###
setup = 'Testing'
if setup == 'Testing':
    print "Starting test mode, will run data through algorithm"
    path.insert(0, "Training_functions")
    from naoqi import ALProxy
    encoders_available = False
elif setup == 'Developing':
    print "Using developer mode, encoders will return fake values"
    path.insert(0, "Training_functions")
    from naoqi import ALProxy
    import BigEncoder
    import SmallEncoders
    encoders_available = True
    print "Fake encoders connected"
elif setup == 'Real':
    print "Using real mode"
    path.insert(0, "hidlibs")  # Insert encoder path.
    from pynaoqi.naoqi import ALProxy
    import top_encoder.encoder_functions as BigEncoder
    import bottom_encoder.hingeencoder as SmallEncoders
    encoders_available = True
    print "Encoders connected"


class Robot():
    """
    Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
    """

    def __init__(self, setup, ip="192.168.1.3", port=9559, initial_position="Stand"):
        """
        Sets up the connection to the robot and sets initial posture. Also calibrates encoders to zero, if available.
        Requires arguments:

        ip : string, contains the IPv4 address of the robot to connect to.
        port : int, contains the port number through which to access the robot.
        """
        # Run different setup code
        self.setup = setup

        # Set up connection manager.
        #self.connection = ALProxy("ALConnectionManager", ip, port)
        #print("Network state: " + self.connection.state())

        self.speech = ALProxy("ALTextToSpeech", ip, port)
        self.speech.say("Connected")

        # Set up proxies to robot.
        self.motion = ALProxy("ALMotion", ip, port)
        #self.posture = ALProxy("ALRobotPosture", ip, port)
        self.memory = ALProxy("ALMemory", ip, port)

        # Set up encoders, if available.
        if encoders_available:
            SmallEncoders.calibrate()
            BigEncoder.calibrate()

        # self.posture.goToPosture(initial_position, 1.0) # Set initial
        # position.

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
        Obtain the current accelerometer data. Returns a list containing the (x, y, z) acceleromenter data,
        in m/s.
        """
        x_data = self.memory.getData(values['AX'][1])
        y_data = self.memory.getData(values['AY'][1])
        z_data = self.memory.getData(values['AZ'][1])

        return [x_data, y_data, z_data]

    @staticmethod
    def get_small_encoders():
        """
        Return the angles recorded by the small hinge encoders, at the base of the sqing, at the time of calling.
        If encoders are not available, will return None *without* producing an error.
        Returns a tuple, where the index of each value is the same as numbered in the source file from previous years.
        """

        if encoders_available:
            encoder0 = SmallEncoders.getAngle0()
            encoder1 = SmallEncoders.getAngle1()
            encoder2 = SmallEncoders.getAngle2()
            encoder3 = SmallEncoders.getAngle3()

            return [encoder0, encoder1, encoder2, encoder3]

    @staticmethod
    def get_big_encoder():
        """
        Returns the numerical value read from the large encoder at the top of the swing, if available. Else returns None,
        *without* producing an error.
        """

        if encoders_available:
            return BigEncoder.getAngle()

    def get_angle(self, nameofpart):
		"""
		Get the current angle of the named part. (Taken from robotcontrol2.py)
		Requires:
		
		nameofpart : the name of the part.
		"""
        a = self.memory.getData(values[str(nameofpart)][1])
        name = values[str(nameofpart)][0]
        return a, name

    def initial_seated_position(self):
        """
        Sets the robot to the initial seated position.
        """
    
        parts = ["Head", "RLeg", "LLeg"]
        self.motion.setStiffnesses(parts, 1.0)  # stiffen
        angle_names = [
            values['HP'][0],
            values['RHP'][0],
            values['LHP'][0],
            values['RKP'][0],
            values['LKP'][0]]
        angles = [-0.6, -0.51, -0.51, -0.09, -0.09]
        speed = 0.5
        self.motion.setAngles(angle_names, angles, speed)

    def move_part(self, parts, angle_names, angles, speed, rest_time):
        """
        Moves the specified parts.
        """
        self.motion.setStiffnesses(parts, 1.0)
        self.motion.setAngles(angle_names, angles, speed)
        tme.sleep(rest_time)


    def extended_position(self):
        """
        Sets the extended position for when on swing.
        """
        angle_names = extended.keys()
        angles = extended.values()
        rest_time = 0
        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        final_angle_names = [values[name][0] for name in angle_names]
        #speed =       [normalise_speed()]
        self.move_part(parts, final_angle_names, angles, 0.6, rest_time)

    def seated_position(self):
        """
        Sets the seated position for when on swing.
        """
        rest_time = 0
        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        angle_names = seated.keys()
        angles = seated.values()
        final_angle_names = [values[name][0] for name in angle_names]
        self.move_part(parts, final_angle_names, angles, 0.6, rest_time)

    def test_move_part(self):
        """
        Movement test.
        """
        self.motion.setStiffnesses("RLeg", 1.0)
        self.motion.setStiffnesses("LLeg", 1.0)
        self.motion.setAngles("LKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("LAnklePitch",-1.18943989277,0.1)
        self.motion.setAngles("RKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("RAnklePitch",-1.18943989277,0.1)

    def store(self, filename):
        """
        Stores data as csv
        filename: name of file to store to
        """

        self.all_data.to_csv('Output_data/' + filename)
        print 'Data saved to {}'.format(filename)

    def algorithm(self, time, acc, gyro, l_encoder, b_encoder):
        recent_data = self.collect_old_data(5)
        print recent_data

    def collect_old_data(self, last_n_results):
        """
        Returns dataframe of last_n_results INCLUDING latest
        """
        return self.all_data.tail(last_n_results)

    def __run_real(self, t, period, filename=None):
        self.all_data = DataFrame(columns=['AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'SE0', 'SE1', 'SE2', 'SE3', 'BE'])
        self.all_data.index.name = 'Time'

        max_runs = t * 1 / period
        if filename == None:
            filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())

        for _ in range(int(max_runs)):
            start_time = tme.time()

            # needs to be list of lists for easy flattening for storage while retaining ease of use for
            # putting into algorithm
            values = [
                start_time,
                self.get_acc(),
                self.get_gyro(),
                self.get_small_encoders(),
                self.get_big_encoder()]

            flat_values = flatten(values)
            # Computationally expensive but incredibly useful for quick data manipulation
            self.all_data.loc[start_time, :] = flat_values[1:]

            self.algorithm(*values)

            cycle_time = tme.time() - start_time
            if cycle_time < period:
                tme.sleep(period - cycle_time)


        if cycle_time > period:
            print('RAN BEHIND SCHEDULE')
        else:
            print('Ran on time')
        self.store(filename)

    def __run_test(self, t, period, filename=None):
        print 'Using test mode, will apply algorithm to data from file {}'.format(filename)
        data = self.read('TestData')

        self.all_data = DataFrame(columns=['AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'SE0', 'SE1', 'SE2', 'SE3', 'BE'])
        self.all_data.index.name = 'Time'

        for index, row in data.iterrows():
            self.all_data.loc[index, :] = row
            self.algorithm(row['Time'], row[['AX', 'AY', 'AZ']], row[['GX', 'GY', 'GZ']], row[['SE1', 'SE2', 'SE3', 'SE4']], row['BE'])
            

    def run(self, t, period, filename=None):
        """
        t: time to run for
        period: period of cycle time
        filename : string, location of the file to read from if training. Ignore if not training.
        """

        if self.setup == 'Testing':
            self.__run_test(t, period, filename)
        else:
            self.__run_real(t, period, filename)

    def read(self, filename):
        """
        Reads old data
        """ 
        return read_csv('Output_data/' + filename, sep=',')

if __name__ == "__main__":
    robot = Robot(setup)
    robot.run(10, 0.1)


