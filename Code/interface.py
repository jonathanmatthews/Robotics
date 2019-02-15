# python2.7
import numpy
"""
A module containing interface that connects robot and encoders to algorithm and storage.

Contains class:
    Interface
"""

from sys import path
import time as tme
from utility_functions import flatten
from encoder_interface import Encoders
from robot_interface import Robot
# Different positions of robot
from positions import positions
# Information of robot limbs (max angle etc)
from limb_data import values

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

class Interface(Robot, Encoders):
    """
    This class ties together the Robot and the Encoders, and adds functionality such as storing, and running tests
    on old data. It inherits from Robot and Encoders so has access to all their methods in the normal way (self.get_gyro() etc).
    """

    def __init__(self, setup):
        # Initialise encoder
        Encoders.__init__(self, BigEncoder, SmallEncoders)
        # Initialise robot
        Robot.__init__(self, values, positions, ALProxy)

        # Store setup mode for later
        self.setup = setup

    def algorithm(self, *args):
        """
        Defines how robot moves with swinging.
        Can collect old data via:
        print self.all_data
        Can move to new position via:
        self.set_posture('extended')
        pos will be name of current position
        """
        pos, time, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
        if b_encoder < -10 and pos == 'extended':
             self.set_posture('seated')
        if b_encoder > 10 and pos == 'seated':
            self.set_posture('extended')
        print time, pos

    def __run_real(self, t, period):
        max_runs = t * 1 / period

        # Data will be added to this with time
        self.all_data = numpy.empty((int(max_runs), 13))
        # Filename of exact running time
        filename = tme.strftime("%d-%m-%Y %H:%M:%S", tme.gmtime())
        initial_time = tme.time()

        for t in range(int(max_runs)):
            start_time = tme.time()

            # record data as list of lists
            values = [
                start_time - initial_time,
                self.get_acc(),
                self.get_gyro(),
                self.get_small_encoders(),
                self.get_big_encoder()]

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
        self.all_data = numpy.empty((1, 13))

        for i in xrange(len(data)):
            # Put new data through algorithm not including position as want to test algo
            self.algorithm(self.position_names[self.position], *data[i, :-1])
            # Add new data to available data
            self.all_data = numpy.append(self.all_data, data[i])

    def run(self, t, period, **kwargs):
        """
        Either kicks off testing from old data or collects off collection of data
        t: time to run for
        period: period of cycle time
        filename : string, location of the file to read from if testing. Ignore if not testing.
        """
        if self.setup == 'Testing':
            # If filename isn't passed through takes this default file
            filename = kwargs.get('filename', '15-02-2019 10:29:57')
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
        Saves numpy matric as txt file
        filename: name of file to store to in Output_data folder
        """

        # All data should be a numpy array
        numpy.savetxt("Output_data/" + filename, self.all_data)
        print 'Data saved to {}'.format(filename)


if __name__ == "__main__":
    interface = Interface(setup)
    interface.run(30, 0.1)
