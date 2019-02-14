# -*- encoding: UTF-8 -*-
"""
record sensor values from the head (yaw) movement and output them to a file.
"""
import sys
import os
import time
sys.path.insert(0, "hidlibs")
from pynaoqi.naoqi import ALProxy
from limb_data import values

ALMEMORY_KEY_NAMES = [
    values['HY'][1],
    # Should below line exist in values datasheet? 07/02 George
    # "Device/SubDeviceList/HeadYaw/Position/Actuator/Value",
]

ROBOT_IP = "192.168.1.3"


def recordData(ROBOT_IP, output_path):
    """ records the data from ALMemory.
    Returns a matrix of the values

    """
    print "Recording data ..."
    memory = ALProxy("ALMemory", ROBOT_IP, 9559)
    with open(output_path, "w") as fp:
        for _ in range(1, 100):
            line = [memory.getData(key) for key in ALMEMORY_KEY_NAMES]
            fp.write(", ".join(str(x) for x in line) + "\n")
            time.sleep(0.05)

    print "Results written to", output_path


def main():
    """ Parse command line arguments,
    run recordData and write the results
    into a csv file

    """
    if len(sys.argv) < 2:
        nao_ip = ROBOT_IP
    else:
        nao_ip = sys.argv[1]

    motion = ALProxy("ALMotion", nao_ip, 9559)
    motion.set_stiffness("Head", 0)
    # Will go to 1.0 then 0 radian
    # in two seconds
    motion.post.angleInterpolation(
        ["HeadYaw"],
        [1.2, 1],
        [1, 2],
        False
    )
    output_path = "Output_data/recordheadmovement.csv"

    recordData(nao_ip, output_path)
    # Gently set stiff off for Head motors
    motion.set_stiffness('Head')


if __name__ == "__main__":
    main()
