# python2.7
import time as tme
from limb_data import values
from positions import positions
from utility_functions import flatten
from sys import path
from robot_interface import Robot
from encoder_interface import Encoders
import numpy
"""
A module containing an interface that connects the robot and encoders to algorithm and storage.

Contains class:
    Interface
"""
"""To change from webots to real world, change import below."""

#from robot_interface_webots import Robot
from os import listdir
from re import compile

files = listdir('.')
r = compile("algorithm_")
list_algorithms = filter(r.match, files)
text = ["{} {}".format(i, algo[:-3]) for i, algo in enumerate(list_algorithms)]
algorithm = str(
    input(
        'Which algorithm would you like to run? Pick number corresponding to algorithm: \n{}\n'.format(
            "\n".join(text))))
algorithm_import = [algo[2:] for algo in text if algorithm in algo][0]
Algorithm = __import__(algorithm_import[:-3]).Algorithm

# Different positions of robot
# Information of robot limbs (max angle etc)

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

        # Store setup mode for later
        self.setup = setup

    def get_ang_vel(self, event_number):
        """
        Function to get the current angular velocity, accessing the last two data
        values recorded. Returns None if not enough data exists yet.
        Requires arguments:
        event_number : int, the row within self.all_data at whcih to calculate.
        """
        if len(self.all_data) < 2:
            return None

        prev_data = self.all_data[event_number - 1]
        curr_data = self.all_data[event_number]

        delta_time = curr_data[0] - prev_data[0]
        delta_angle = curr_data[-5] - prev_data[-5]

        return delta_angle / delta_time

    def centre_of_mass(self, angle1, angle2, angle3):
        '''Returns the centre of mass relative to the big encoder.'''
        L1 = 1.5  # length of pendulum 1 in m
        L2 = 0.12  # length of pendulum 2 in m
        L3 = 0.20  # length of pendulum 3 in m
        a1 = angle1 * numpy.pi/180
        a2 = angle2 * numpy.pi/180
        a3 = angle3 * numpy.pi/180
        x_seat = L3 * numpy.sin(a1 + a2 + a3) + L2 * numpy.sin(a1 + a2) + L1 * numpy.sin(a1)
        y_seat = L3 * numpy.cos(a1 + a2 + a3) + L2 * numpy.cos(a1 + a2) + L1 * numpy.cos(a1)
        if self.position == "seated":
            x_com = x_seat + 0.00065
            y_com = y_seat + 0.1166
        elif self.position == "extended":
            x_com = x_seat + 0.0183
            y_com = y_seat + 0.1494
        else:
            raise ValueError("Position not found")
        return [x_com, y_com]

    def __run_real(self, t, period):
        max_runs = t * 1 / period

        # Data will be added to this with time
        self.all_data = numpy.empty((int(max_runs), 17))
        # Filename of exact running time
        filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())

        initial_time = tme.time()
        for t in range(int(max_runs)):
            start_time = tme.time()

            # record data as list of lists
            values = [
                start_time - initial_time,
                t,
                self.get_acc(),
                self.get_gyro(),
                self.get_small_encoders(),
                self.get_big_encoder(),
                self.get_ang_vel(t)]
            
            values.append(self.centre_of_mass(values[5], values[4][0], values[4][1]))

            # use flatten in utility functions to reduce to one long list
            # (better for storage) and add current position
            flat_values = flatten(values)

            # run new data through algorithm
            self.algorithm(self.position, *flat_values)

            flat_values.append(self.position_names[self.position])
            # add data to row of numpy matrix
            self.all_data[t, :] = flat_values

            # wait until end of cycle time before running again
            cycle_time = tme.time() - start_time
            if cycle_time < period:
                tme.sleep(period - cycle_time)

        # assume final cycle took same time as rest to check if behind or not
        if cycle_time > period:
            print('RAN BEHIND SCHEDULE')
        else:
            print('Ran on time')
        # store data in txt file
        self.store(filename)

    def __run_test(self, t, period, filename):
        """
        Runs old data line by line through algorithm so that algorithm can be tested
        """
        # Read old data
        data = self.read(filename)
        print 'Using test mode, will apply algorithm to data from file {}'.format(filename)

        # Needs to update line by line so only have access to data you would if
        # running real time
        self.all_data = numpy.empty((len(data), 17))

        for i in xrange(len(data)):
            # Put new data through algorithm not including position as want to
            # test algo
            self.algorithm(self.position_names[self.position], *data[i, :-1])
            # Add new data to available data
<<<<<<< HEAD
            line_data = numpy.append(data[i, :-1], [self.position_names[self.position]], axis=0)
            self.all_data[i] = line_data
            #self.all_data = numpy.append(self.all_data, line_data, axis=0)
=======
            self.all_data = numpy.append(self.all_data, numpy.array(
                [tuple(current_values.values())], dtype=data_type), axis=0)
        self.store(filename)
>>>>>>> baf7841f5378b438589cf83d2b31d587cc4ecb62

    def run(self, t, period, **kwargs):
        """
        Either kicks off testing from old data or collects off collection of data
        t: time to run for
        period: period of cycle time
        filename : string, location of the file to read from if testing. Ignore if not testing.
        """
        if self.setup == 'Testing':
            # access latest file if underneath file name is blanked out
            files = sorted(listdir('Output_data/'))
            latest = files[-1]
            filename = kwargs.get('filename', latest)
            self.__run_test(t, period, filename)
        else:
            self.__run_real(t, period)

    def read(self, filename):
        """
        Reads old data
        """
        return numpy.loadtxt('Output_data/' + filename)

    def store(self, filename):
        """
        Saves numpy matrix as txt file
        filename: name of file to store to in Output_data folder
        """

        # All data should be a numpy array
        numpy.savetxt("Output_data/" + filename, self.all_data)
        print 'Data saved to {}'.format(filename)


if __name__ == '__main__':
    interface = Interface(setup)
<<<<<<< HEAD
    #interface.run(20, 0.2)
    # interface.set_posture("extended")
    interface.run(1.0, 1.0)
=======
    interface.run(20, 0.15)
>>>>>>> baf7841f5378b438589cf83d2b31d587cc4ecb62
