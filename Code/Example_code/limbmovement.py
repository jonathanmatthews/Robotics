# -*- encoding: UTF-8 -*-

'''Walk: Small example to make Nao walk'''
import sys
import motion
import time
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception as e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception as e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    Arm1 = [-40, 25, 0, -40]
    Arm1 = [x * motion.TO_RAD for x in Arm1]

    pFractionMaxSpeed = 1

    motionProxy.angleInterpolationWithSpeed(
        JointNames, Arm1, pFractionMaxSpeed)
    motionProxy.angleInterpolationWithSpeed(
        JointNames, Arm1, pFractionMaxSpeed)
    time.sleep(2.0)


if __name__ == "__main__":
    robotIp = "192.168.1.3"

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: 192.168.1.3)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
