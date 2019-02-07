import os
import sys
import time
from datanames import values
from naoqi import ALProxy
from change_stiffness import *

ROBOT_IP = "192.168.1.3"
PORT = 9559


class Robotcontrol():
    def __init__(self, ROBOT_IP="192.168.1.3", PORT=9559):
        self.motion = ALProxy("ALMotion", ROBOT_IP, PORT)
        self.memory = ALProxy("ALMemory", ROBOT_IP, PORT)

        # part_name = angle_name, angle_extend, range, angle seat, speed
        # TODO: pretty sure the name, angle_extend, range should be combined with the datanames file,
        # for angle seat I think we should define a set of positions in a seperate file and then we can
        # just import positions when we need to so it's more reusable :) 07/02 George
        # e.g. seat = {
        #   'HP': 0.4974,
        #   'RSR': -0.25775,
        #   'LSR': 0.51231
        # etc
        # }
        self.HP = ["HeadPitch", -0.6685, 1.18, 0.4974, ]
        self.RSR = ["RShoulderRoll", 0.01837, 0.27612, -0.25775, ]
        self.LSR = ["LShoulderRoll", 0.08279, 0.42952, 0.51231, ]
        self.RSP = ["RShoulderPitch", 0.80999, 0.52310, 1.33309, ]
        self.LSP = ["LShoulderPitch", 0.81298, 0.35589, 1.16887, ]
        self.REY = ["RElbowYaw", 1.38669, 0.00921, 1.39590, ]
        self.LEY = ["LElbowYaw", -1.13060, 0.00460, -1.12600, ]
        self.RER = ["RElbowRoll", 0.21327, 1.33135, 1.54462, ]
        self.LER = ["LElbowRoll", -0.26841, 1.27621, -1.54462, ]
        self.RHP = ["RHipPitch", -0.60129, 0.472, -1.08756, ]
        self.LHP = ["LHipPitch", -0.60129, 0.472, -1.08756, ]
        self.RKP = ["RKneePitch", -0.09208, 1.64, 1.48334, ]
        self.LKP = ["LKneePitch", -0.09208, 1.64, 1.48334, ]
        self.RWY = ["RWristYaw", 0.48163, 0.02148, 0.51231, ]
        self.LWY = ["LWristYaw", -0.82227, 0.01994, -0.84221, ]
        self.RH = ["RHand", 0.00860, 0.001, 0.00860, ]
        self.LH = ["LHand", 0.00860, 0.001, 0.00860, ]

    def get_angle(self, nameofpart):
        a = self.memory.getData(values[str(nameofpart)][1])
        name = values[str(nameofpart)][0]
        return a, name

    #motion.setStiffnesses("Body", 1)
    # change_stiffness('stiffen')
    # print get_angle('BC')

    def initial_seated_position(self):
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

    # initial_seated_position()
    # print motion.getSummary()
    # knee range is longest so normalise based on this parameter

    def move_part(self, parts, angle_names, angles, speed, rest_time):
        self.motion.setStiffnesses(parts, 1.0)
        self.motion.setAngles(angle_names, angles, speed)
        time.sleep(rest_time)

    def extended_position(self):
        rest_time = 1.30
        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        angle_names = [
            self.HP[0],
            self.RSR[0],
            self.LSR[0],
            self.RSP[0],
            self.LSP[0],
            self.REY[0],
            self.LEY[0],
            self.RER[0],
            self.LER[0],
            self.RHP[0],
            self.LHP[0],
            self.RKP[0],
            self.LKP[0],
            self.RWY[0],
            self.LWY[0],
            self.RH[0],
            self.LH[0]]
        angles = [
            self.HP[1],
            self.RSR[1],
            self.LSR[1],
            self.RSP[1],
            self.LSP[1],
            self.REY[1],
            self.LEY[1],
            self.RER[1],
            self.LER[1],
            self.RHP[1],
            self.LHP[1],
            self.RKP[1],
            self.LKP[1],
            self.RWY[1],
            self.LWY[1],
            self.RH[1],
            self.LH[1]]
        #speed =       [normalise_speed()]
        self.move_part(self.motion, parts, angle_names, angles, 0.6, rest_time)

    def seated_position(self):
        rest_time = 1.30

        parts = ["Head", "RArm", "LArm", "RLeg", "LLeg"]
        # if dictionary is used can just change to:
        # angle_names = seat.keys()
        # angles = seat.values()
        angle_names = [
            self.HP[0],
            self.RSR[0],
            self.LSR[0],
            self.RSP[0],
            self.LSP[0],
            self.REY[0],
            self.LEY[0],
            self.RER[0],
            self.LER[0],
            self.RHP[0],
            self.LHP[0],
            self.RKP[0],
            self.LKP[0],
            self.RWY[0],
            self.LWY[0],
            self.RH[0],
            self.LH[0]]
        angles = [
            self.HP[3],
            self.RSR[3],
            self.LSR[3],
            self.RSP[3],
            self.LSP[3],
            self.REY[3],
            self.LEY[3],
            self.RER[3],
            self.LER[3],
            self.RHP[3],
            self.LHP[3],
            self.RKP[3],
            self.LKP[3],
            self.RWY[3],
            self.LWY[3],
            self.RH[3],
            self.LH[3]]
        #speed =       []
        self.move_part(self.motion, parts, angle_names, angles, 0.6, rest_time)

    def record_data(self, nameofpart):
        """ records the data from ALMemory.
        Returns a matrix of the values

        """
        print "Recording data from NAO..."

        output = os.path.abspath('Output_data/record_data.csv')

        with open(output, "w") as fp:
            for i in range(1, 100):
                value = self.get_angle(str(nameofpart))
                fp.write(", ".join(str(x) for x in value) + "\n")
                time.sleep(0.05)

        print "Results written to", output

    def test_move_part(self):
        self.motion.setStiffnesses("RLeg", 1.0)
        self.motion.setStiffnesses("LLeg", 1.0)
        self.motion.setAngles("LKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("LAnklePitch",-1.18943989277,0.1)
        self.motion.setAngles("RKneePitch", 0.800258815289, 0.1)
        # motion.setAngles("RAnklePitch",-1.18943989277,0.1)


print 6
r = Robotcontrol(ROBOT_IP="192.168.1.3", PORT=9559)
print 1
r.extended_position()
try:
    while True:
        print 2
        a = raw_input("extend")

        b = raw_input("sit")
        r.seated_position()

except KeyboardInterrupt:
    pass
