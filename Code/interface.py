# python2.7
from re import compile
from os import listdir
import time as tme
from limb_data import values
from positions import positions
from utility_functions import flatten, read_file, current_data_types, get_latest_file, convert_list_dict
from sys import path
from robot_interface import Robot
from encoder_interface import Encoders
import numpy
from collections import OrderedDict
"""
A module containing an interface that connects the robot and encoders to algorithm and storage.

Contains class:
    Interface
"""
"""To change from webots to real world, change import below."""

#from robot_interface_webots import Robot

files = listdir('.')
r = compile("algorithm_")
list_algorithms = filter(r.match, files)
text = [algo for algo in list_algorithms if algo[:-4] != '.pyc'] 
text = ["{} {}".format(i, algo) for i, algo in enumerate(list_algorithms)]
algorithm = str(
    input(
        'Which algorithm would you like to run? Pick number corresponding to algorithm: \n{}\n'.format(
            "\n".join(text))))
algorithm_import = [algo[2:] for algo in text if algorithm in algo][0]
Algorithm = __import__(algorithm_import[:-3]).Algorithm


"""
Set mode to run here
Developing: for running through real code away from encoders
Testing: for seeing how algorithm reacts to old dataset
Real: for in lab running from lab PC
Other two are self explanatory
"""
setup = 'Developing'
# Each setup either has access to real robot (True) or fake robot (False) and
# has access to real encoders (True) or fake encoders (False)
setups = {
    'Testing': [False, False],
    'Developing': [False, False],
    'Real': [True, True],
    'Robot_no_encoders': [True, False],
    'Encoders_no_robot': [False, True]
}
robot, encoders = setups[setup]
try:
    if robot:
        # Add path to real naoqi if connecting to real robot
        path.insert(0, "hidlibs")
        #from naoqi import ALProxy
        from pynaoqi.naoqi import ALProxy
    else:
        # Add path to fake naoqi if not connecting to robot
        path.insert(0, "Training_functions")
        from naoqi import ALProxy
    if encoders:
        # Add path to real encoder functions if connected to them
        path.insert(0, "hidlibs")
        import top_encoder.encoder_functions as BigEncoder
        import bottom_encoder.hingeencoder as SmallEncoders
    else:
        # Add path to fake encoder functions if not connecting to encoders
        path.insert(0, "Training_functions")
        import BigEncoder
        import SmallEncoders
except ImportError as e:
    print "Couldn't import, you are most likely in the wrong directory, try again from Code directory"
    raise e


class Interface(Algorithm):
    """
    This class ties together the Robot and the Encoders, and adds functionality such as storing, and running tests
    on old data. It inherits from Robot and Encoders so has access to all their methods in the normal way (self.get_gyro() etc).
    """

    def __init__(self, setup):
        # Initialise algorithm
        Algorithm.__init__(
            self,
            BigEncoder,
            SmallEncoders,
            values,
            positions,
            ALProxy)

        # Store setup mode for later
        self.setup = setup

    def hands_grip_swing():
        if touch.TouchChanged(“FrontTactilTouched”) == 1:
            print 3

    def get_ang_vel(self, time, current_angle):
        """
        Function to get the current angular velocity, taking last recorded value and new
        value. Returns None if not enough data exists yet.
        Requires arguments:
        time: time since start of algorithm
        current_angle: current big encoder value
        """
        if len(self.all_data) == 0:
            return 0

        # time_data = self.all_data['time']
        # angle_data = self.all_data['be']
        latest_values = self.all_data[-1]

        # delta_time = time - time_data[-1]
        # delta_angle = current_angle - angle_data[-1]

        delta_time = time - latest_values['time']
        delta_angle = current_angle - latest_values['be']

        return delta_angle / delta_time

    def centre_of_mass(self, angle1, angle2, angle3):
        '''Returns the centre of mass relative to the big encoder.'''
        L1 = 1.5  # length of pendulum 1 in m
        L2 = 0.12  # length of pendulum 2 in m
        L3 = 0.20  # length of pendulum 3 in m
        a1 = angle1 * numpy.pi / 180
        a2 = angle2 * numpy.pi / 180
        a3 = angle3 * numpy.pi / 180
        x_seat = L3 * numpy.sin(a1 + a2 + a3) + L2 * \
            numpy.sin(a1 + a2) + L1 * numpy.sin(a1)
        y_seat = - L3 * numpy.cos(a1 + a2 + a3) - L2 * \
            numpy.cos(a1 + a2) - L1 * numpy.cos(a1)
        if self.position == "seated":
            x_com = x_seat - (0.00065 * numpy.sin(a1 + a2 + a3))
            y_com = y_seat + (0.1166 * numpy.cos(a1 + a2 + a3))
        elif self.position == "extended":
            x_com = x_seat - (0.0183 * numpy.sin(a1 + a2 + a3))
            y_com = y_seat + (0.1494 * numpy.cos(a1 + a2 + a3))
        else:
            raise ValueError("Position not found")
        return [x_com, y_com]

    def __run_real(self, t, period):
        max_runs = t * 1 / period + 1.0

        data_type = current_data_types()
        # Data will be added to this with time
        self.all_data = numpy.empty((0, ), dtype=data_type)

        # Filename of exact running time
        filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())


        initial_time = tme.time()
        for event in range(int(max_runs)):
            start_time = tme.time()

            time = start_time - initial_time
            ax, ay, az = self.get_acc()
            gx, gy, gz = self.get_gyro()
            se0, se1, se2, se3 = self.get_small_encoders()
            be = self.get_big_encoder()
            cmx, cmy = self.centre_of_mass(be, se0, se1)
            av = self.get_ang_vel(time, be)

            # position recorded is position before any changes
            current_values = convert_list_dict([time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, self.position])

            self.algorithm(current_values)
            self.all_data = numpy.append(self.all_data, numpy.array(
                [tuple(current_values.values())], dtype=data_type), axis=0)

            # wait until end of cycle time before running again
            cycle_time = tme.time() - start_time
            if cycle_time < period:
                tme.sleep(period - cycle_time)

        # assume final cycle took same time as rest to check if behind or not
        time_taken = tme.time() - initial_time
        if time_taken > 1.01 * t:
            print('RAN BEHIND SCHEDULE')
            print('Correct timing: {}s'.format(t))
            print('Actual timing: {}s'.format(time_taken))
        else:
            print('Ran on time')
        # store data in txt file
        self.store(filename)

    def __run_test(self, t, period, filename, output_directory):
        """
        Runs old data line by line through algorithm so that algorithm can be tested
        """
        # Read old data
        data = read_file(output_directory + filename)
        print 'Using test mode, will apply algorithm to data from file {}'.format(filename)

        # Needs to update line by line so only have access to data you would if
        # running real time
        data_type = current_data_types()
        # Data will be added to this with time
        self.all_data = numpy.empty((0, ), dtype=data_type)

        for i in xrange(len(data)):
            row_no_pos = list(data[i])[:-1]
            current_values = convert_list_dict(row_no_pos + [self.position])
            # Put new data through algorithm not including position as want to
            self.algorithm(current_values)
            # Add new data to available data
            self.all_data = numpy.append(self.all_data, numpy.array(
                [tuple(current_values.values())], dtype=data_type), axis=0)
        self.store(filename)

    def run(self, t, period, **kwargs):
        """
        Either kicks off testing from old data or collects off collection of data
        t: time to run for
        period: period of cycle time
        filename : string, location of the file to read from if testing. Ignore if not testing.
        """
        if self.setup == 'Testing':
            latest, output_directory = get_latest_file('Code')
            filename = kwargs.get('filename', latest)
            self.__run_test(t, period, filename, output_directory)
        else:
            self.__run_real(t, period)

    def store(self, filename):
        """
        Saves numpy matrix as txt file
        filename: name of file to store to in Output_data folder
        """
        with open('Output_data/' + filename, 'w') as f:
            rows = [[str(i) for i in list(line)[:-1]] + [line[-1]]
                    for line in self.all_data]
            for row in rows:
                f.write(','.join(row) + '\n')
        print 'Data saved to {}'.format(filename)


if __name__ == '__main__':
    interface = Interface(setup)
    interface.run(5, 0.10)
