# python2.7
from re import search
from os import listdir
import time as tme
from limb_data import values
#from positions import positions
from positions2 import positions
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

class AlgorithmFinished(Exception): pass

"""To change from webots to real world, change import below."""
#from robot_interface_webots import Robot


# Allows user to select the algorithm file in Algorithms that they want to run
files = listdir('Algorithms')
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

# Imports correct Algorithm class that interface inherits from
algorithm_import = algo_dict[int(algorithm)]
path.insert(0, 'Algorithms')
Algorithm = __import__(algorithm_import).Algorithm


"""
Set mode to run here
Developing: for running through real code away from encoders
Testing: for seeing how algorithm reacts to old dataset
Real: for in lab running from lab PC
Other two are self explanatory
"""

# Each setup either has access to real robot (True) or fake robot (False) and
# has access to real encoders (True) or fake encoders (False)
setups = {
    'Testing': [False, False],
    'Developing': [False, False],
    'Real': [True, True],
    'Robot_no_encoders': [True, False],
    'Encoders_no_robot': [False, True]
}
# Can set manually or use argv when running interface or test_plot.sh
setup = 'Real'
if argv[-1] in setups.keys():
    setup = argv[-1]
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
    on old data. It inherits from Algorithm which inherits from Robot and Encoder so has access to all their methods in the normal way (self.get_gyro() etc).
    """

    def __init__(self, setup):
        # Connect properties of algorithm to interface
        Algorithm.__init__(
            self,
            BigEncoder,
            SmallEncoders,
            values,
            positions,
            ALProxy)

        # Store setup mode for later, (Testing, Developing etc)
        self.setup = setup

        # Robot initialises and moves to start position
        self.speech.say("Checking position, then starting")
        # Give robot time to get into position before checking it
        tme.sleep(2.0)
        try:
            self.check_setup('seated')
        except ValueError as e:
            # When position doesn't set properly
            self.motion.setStiffnesses("Body", 0.0)
            self.speech.say('Failed, loosening')
            raise e

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
            # Remove first dictionary element from algorithm and store it
            info = self.order.pop(0)
        except IndexError:
            # Interface handles exception to break out of loop and stops and save
            raise AlgorithmFinished

        # Remove class from dictionary and store it
        self.algo_class = info.pop('algo')
        # Rest of dictionary left are kwargs
        kwargs = info
        # Run initializer of next algorithm with kwargs
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
        # No angular velocity if no old data
        if len(self.all_data) == 0:
            return 0

        latest_values = self.all_data[-1]

        delta_time = time - latest_values['time']
        delta_angle = current_angle - latest_values['be']

        return delta_angle / delta_time

    def algo_name(self):
        """ 
        Extract name of current algorithm, added to storage good for graphs
        """
        try:
            algo = self.algo_class.__name__
        except:
            algo = 'None'
        return algo

    def __run_algorithm(self, switch, current_values):
        """
        Handles which algorithm to run, input to algorithm, output from algorithm,
        and appending to all_data.
        Args:
            switch: output from previous cycle of algorithm
            current_values: all values to be passed into the algorithm
        Returns:
            switch: output from this cycle of algorithm
        """
        # Set current algorithm to next algorithm
        if switch == 'switch':
            self.algorithm = self.next_algo(current_values, self.all_data)

        # Algorithm returns name of position to switch to or 'switch' to change algorithm
        switch = self.algorithm(current_values, self.all_data)

        # If text returned is a possible position switch to it
        if switch in positions.keys():
            self.set_posture(switch, self.position)

        # Add current values to list of all values
        self.all_data = numpy.append(self.all_data, numpy.array(
            [tuple(current_values.values())], dtype=self.data_type), axis=0)
        return switch


    def __run_real(self, t, period):
        # Maximum number of loops to collect and run through algorithm
        max_runs = t * 1 / period + 1.0

        # For good numpy storage need column names and data types
        self.data_type = current_data_types()
        # Data will be appended to this with time
        self.all_data = numpy.empty((0, ), dtype=self.data_type)

        # Filename of exact running time
        filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())
        # Will switch to first algorithm on first loop
        switch = 'switch'

        initial_time = tme.time()
        for event in range(int(max_runs)):
            start_time = tme.time()

            # Collect all relevant values
            time = start_time - initial_time
            ax, ay, az = self.get_acc()
            gx, gy, gz = self.get_gyro()
            se0, se1, se2, se3 = self.get_small_encoders()
            be = self.get_big_encoder()
            cmx, cmy = centre_of_mass_respect_seat(self.position, self.masses)
            av = self.get_ang_vel(time, be)

            algo = self.algo_name()

            # position recorded is position before any changes
            # Convert all values into dictionary (dictionary as then all_data and values are indexed in the same
            # way) aka values['Time'] or all_data['Time']
            current_values = convert_list_dict(
                [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, self.position])

            try:
                switch = self.__run_algorithm(switch, current_values)
            except AlgorithmFinished:
                print('\033[Algorithm finished, stopping\033[0m')
                break

            # wait until end of cycle time before running again
            cycle_time = tme.time() - start_time
            if cycle_time < period:
                tme.sleep(period - cycle_time)

        # Check whether everything is running on schedule or not
        time_taken = tme.time() - initial_time
        print('\033[Finished in {:.2f}s\033[0m'.format(time_taken))
        # Check how fast code is running
        average_cycle_time = numpy.mean(numpy.diff(self.all_data['Time']))
        print('\033[Expected sampling period: {:.3f}s\nActual sampling period: {:.3f}s\033[0m'.format(period, average_cycle_time))

        # store data in txt file, all original data has ' Org' added to name
        self.store(filename + ' Org')

    def __run_test(self, t, period, filename, output_directory):
        """
        Runs old data line by line through algorithm so that algorithm can be tested
        """
        # Read old data
        print('\033[Using test mode, will apply algorithm to data from file {}\033[0m'.format(filename))
        data = read_file(output_directory + filename)

        # Needs to update line by line so only have access to data you would if
        # running real time
        self.data_type = current_data_types()
        # Data will be added to this with time
        self.all_data = numpy.empty((0, ), dtype=self.data_type)

        switch = 'switch'
        for i in xrange(len(data)):
            algo = self.algo_name()

            row_no_pos_algo = list(data[i])[:-2]
            # Make current row out of real values from data minus the position and algorithm
            # as those are the things we are running testing to watch
            current_values = convert_list_dict(
                row_no_pos_algo + [algo, self.position])

            try:
                switch = self.__run_algorithm(switch, current_values)
            except AlgorithmFinished:
                break

        # Data loaded in will have ' Org' file so remove that and replace with ' Tst'
        self.store(filename[:-4] + ' Tst')

    def run(self, t, period, **kwargs):
        """
        Either kicks off testing from old data or collects off collection of data
        t: time to run for
        period: period of cycle time
        filename : string, location of the file to read from if testing. Ignore if not testing.
        """
        if self.setup == 'Testing':
            latest, output_directory = get_latest_file('Code', test=False)
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
    # Raising error after loosening as then script that plots
    # afterwards doesn't bother
    interface = Interface(setup)
    interface.speech.say('Battery level at {:.0f}%'.format(interface.get_angle('BC')[0]*100))
    try:
        interface.run(30.0, 0.08)
    except KeyboardInterrupt:
        interface.speech.say('Loosening')
        interface.motion.setStiffnesses("Body", 0.0)
        raise KeyboardInterrupt
