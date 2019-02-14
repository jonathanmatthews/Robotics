from robot_interface import Robot

from positions import positions
from sys import path
from limb_data import values
import time as tme
from utility_functions import flatten
from pandas import DataFrame, read_csv
setup = 'Robot_no_encoders'
setups = {
    'Testing': [False, False],
    'Developing': [False, False],
    'Real': [True, True],
    'Robot_no_encoders': [True, False],
    'Encoders_no_robot': [False, True]
}
robot, encoders = setups[setup]
if robot:
    path.insert(0, "hidlibs")  # Insert encoder path.
    from pynaoqi.naoqi import ALProxy
else:
    path.insert(0, "Training_functions")
    from naoqi import ALProxy
if encoders:
    path.insert(0, "hidlibs")  # Insert encoder path.
    import top_encoder.encoder_functions as BigEncoder
    import bottom_encoder.hingeencoder as SmallEncoders
else:
    path.insert(0, "Training_functions")
    import BigEncoder
    import SmallEncoders


r = Robot(setup)
import time
r.set_posture('extended', 1)
