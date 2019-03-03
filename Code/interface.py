# python2.7
from re import search
from os import listdir
import time as tme
from limb_data import values
from positions import positions
from utility_functions import flatten, read_file, current_data_types, get_latest_file, convert_list_dict, centre_of_mass_respect_seat
from sys import path, argv
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
list_algorithms = [x for x in files if search(
    r"(?<=^algorithm_).+(?=\.py$)", x)]
algo_dict = {}
for i, algo in enumerate(list_algorithms):
    algo_dict[i] = algo[:-3]
text = ["{} {}".format(key, algo_dict[key]) for key in algo_dict]

if argv[-1][0] is not "@":
    algorithm = str(
        input(
            'Which algorithm would you like to run? Pick number corresponding to algorithm: \n{}\n'.format(
                "\n".join(text))))
else:
    algorithm = argv[-1][1:]

print("running " + algo_dict[int(algorithm)] + "\n")
# By running this script with the final command line argument '@n' will run the nth algorithm that would
# otherwise appear in the list.

algorithm_import = algo_dict[int(algorithm)]
Algorithm = __import__(algorithm_import).Algorithm


"""
Set mode to run here
Developing: for running through real code away from encoders
Testing: for seeing how algorithm reacts to old dataset
Real: for in lab running from lab PC
Other two are self explanatory
"""
setup = 'Testing'
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
        self.speech.say

        # Store setup mode for later
        self.setup = setup

        self.speech.say("Connected and setup, waiting 2 seconds")
        tme.sleep(3)


    def next_algo(self, values, all_data):
        """
        This function switches to the next algorithm defined in the algorithm file.
        self.order contains the dictionary with the defined order of algorithms, this extracts
        the latest algorithm data, initialises the class with the extra arguments and returns a function
        that only requires values to be put in.
        Arguments:
            values: list of current values, big encoder etc
        Returns:
            reference to function to switch to
        """
        try:
            info = self.order.pop(0)
        except IndexError as e:
            raise IndexError(e, 'Ran out of algorithms')

        self.algo_class = info.pop('algo')
        kwargs = info
        algo_class_initialized = self.algo_class(values, all_data, **kwargs)
        return algo_class_initialized.algo

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

        latest_values = self.all_data[-1]

        delta_time = time - latest_values['time']
        delta_angle = current_angle - latest_values['be']

        return delta_angle / delta_time


    def __run_real(self, t, period):
        max_runs = t * 1 / period + 1.0

        data_type = current_data_types()
        # Data will be added to this with time
        self.all_data = numpy.empty((0, ), dtype=data_type)

        # Filename of exact running time
        filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())
        switch = 'switch'

        initial_time = tme.time()
        for event in range(int(max_runs)):
            start_time = tme.time()

            time = start_time - initial_time
            ax, ay, az = self.get_acc()
            gx, gy, gz = self.get_gyro()
            se0, se1, se2, se3 = self.get_small_encoders()
            be = self.get_big_encoder()
            cmx, cmy = centre_of_mass_respect_seat(self.position)
            av = self.get_ang_vel(time, be)
            try:
                algo = self.algo_class.__name__
            except:
                algo = 'None'

            # position recorded is position before any changes
            current_values = convert_list_dict(
                [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, self.position])

            if switch == 'switch' and event != max_runs - 1:
                self.algorithm = self.next_algo(current_values, self.all_data)
            switch = self.algorithm(current_values, self.all_data)

            if switch in positions.keys():
                self.set_posture(switch)
        
            self.all_data = numpy.append(self.all_data, numpy.array(
                [tuple(current_values.values())], dtype=data_type), axis=0)

            # wait until end of cycle time before running again
            cycle_time = tme.time() - start_time
            if cycle_time < period:
                tme.sleep(period - cycle_time)

        # assume final cycle took same time as rest to check if behind or not
        time_taken = tme.time() - initial_time
        if time_taken > 1.03 * t:
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
        print 'Using test mode, will apply algorithm to data from file {}'.format(filename)
        data = read_file(output_directory + filename)

        # Needs to update line by line so only have access to data you would if
        # running real time
        data_type = current_data_types()
        # Data will be added to this with time
        self.all_data = numpy.empty((0, ), dtype=data_type)

        switch = 'switch'
        for i in xrange(len(data)):
            try:
                algo = self.algo_class.__name__
            except:
                algo = 'None'

            row_no_pos = list(data[i])[:-2]
            current_values = convert_list_dict(row_no_pos + [algo, self.position])
            # Put new data through algorithm not including position as want to

            if switch == 'switch' and i != (len(data) - 1):
                self.algorithm = self.next_algo(current_values, self.all_data)
            switch = self.algorithm(current_values, self.all_data)
            
            if switch in positions.keys():
                self.set_posture(switch)

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
    interface.run(100, 0.10)
    interface.motion.setStiffnesses("Body", 0.0)

