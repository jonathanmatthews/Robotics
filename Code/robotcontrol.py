import os
import sys
import time
from datanames import values
from naoqi import ALProxy
from change_stiffness import *

ROBOT_IP = "192.168.1.3"
PORT = 9559

motion = ALProxy("ALMotion", ROBOT_IP, PORT)
memory = ALProxy("ALMemory", ROBOT_IP, PORT)

#example usage change_stiffness('stiffen')
def get_angle(nameofpart):
    a = memory.getData(values[str(nameofpart)][1])
    name = values[str(nameofpart)][0]
    return a, name

#motion.setStiffnesses("Body", 1)
#change_stiffness('mstiffen')
#print get_angle('BC')

def initial_seated_position():
    parts = ["Head", "RLeg", "LLeg"]
    motion.setStiffnesses(parts, 1.0) #stiffen
    angle_names = [values['HP'][0], values['RHP'][0], values['LHP'][0], values['RKP'][0], values['LKP'][0]]
    angles = [-0.6, -0.51, -0.51, -0.09, -0.09] 
    speed = 0.5
    motion.setAngles(angle_names, angles, speed)

#initial_seated_position()
#print motion.getSummary()

# part_name = angle_name, angle_extend, range, angle seat
HP =  ["HeadPitch",     -0.6685,  1.18,     0.4974,  ]
RSR = ["RShoulderRoll",  0.01837, 0.27612, -0.25775, ]
LSR = ["LShoulderRoll",  0.08279, 0.42952,  0.51231, ]
RSP = ["RShoulderPitch", 0.80999, 0.52310,  1.33309, ]
LSP = ["LShoulderPitch", 0.81298, 0.35589,  1.16887, ]
REY = ["RElbowYaw",      1.38669, 0.00921,  1.39590, ]
LEY = ["LElbowYaw",     -1.13060, 0.00460, -1.12600, ]
RER = ["RElbowRoll",     0.21327, 1.33135,  1.54462, ]
LER = ["LElbowRoll",    -0.26841, 1.27621, -1.54462, ]
RHP = ["RHipPitch",     -0.60129, 0.472,   -1.08756, ]
LHP = ["LHipPitch",     -0.60129, 0.472,   -1.08756, ]
RKP = ["RKneePitch",    -0.09208, 1.64,     1.48334, ]
LKP = ["LKneePitch",    -0.09208, 1.64,     1.48334, ]
RWY = ["RWristYaw",      0.48163, 0.02148,  0.51231, ]
LWY = ["LWristYaw",     -0.82227, 0.01994, -0.84221, ]
RH =  ["RHand",          0.00860, 0.001,    0.00860, ]
LH =  ["LHand",          0.00860, 0.001,    0.00860, ]


def move_part(motion, parts, angle_names, angles, speed, rest_time):
    motion.setStiffnesses(parts, 1.0)
    motion.setAngles(angle_names, angles, speed)
    time.sleep(rest_time)

def extended_position(motion):
    rest_time = 0
    parts =       ["Head", "RArm","LArm", "RLeg", "LLeg"]
    angle_names = [HP[0], RSR[0], LSR[0], RSP[0], LSP[0], REY[0], LEY[0], RER[0], LER[0], RHP[0], LHP[0], RKP[0], LKP[0], RWY[0], LWY[0], RH[0], LH[0]]
    angles =      [HP[1], RSR[1], LSR[1], RSP[1], LSP[1], REY[1], LEY[1], RER[1], LER[1], RHP[1], LHP[1], RKP[1], LKP[1], RWY[1], LWY[1], RH[1], LH[1]]
    #speed =       [normalise_speed()]
    move_part(motion, parts, angle_names, angles, 0.6, rest_time)


def seated_position(motion):
    rest_time = 0
    
    parts =       ["Head", "RArm","LArm", "RLeg", "LLeg"]
    angle_names = [HP[0], RSR[0], LSR[0], RSP[0], LSP[0], REY[0], LEY[0], RER[0], LER[0], RHP[0], LHP[0], RKP[0], LKP[0], RWY[0], LWY[0], RH[0], LH[0]]
    angles =      [HP[3], RSR[3], LSR[3], RSP[3], LSP[3], REY[3], LEY[3], RER[3], LER[3], RHP[3], LHP[3], RKP[3], LKP[3], RWY[3], LWY[3], RH[3], LH[3]]
    #speed =       []
    move_part(motion, parts, angle_names, angles, 1, rest_time)



try:
    while True:
        a = raw_input("pleasese")
        extended_position(motion)
        b = raw_input("pslepels")
        seated_position(motion)

except KeyboardInterrupt:
    pass




def record_data(nameofpart):
    """ records the data from ALMemory.
    Returns a matrix of the values

    """
    print "Recording data from NAO..."
           
    output = os.path.abspath('Output_data/record_data.csv')

    with open(output, "w") as fp:
        for i in range (1, 100):
            value = get_angle(str(nameofpart))
            fp.write(", ".join(str(x) for x in value) + "\n")
            time.sleep(0.05)

    print "Results written to", output    


def test_move_part():
    motion.setStiffnesses("RLeg", 1.0)
    motion.setStiffnesses("LLeg", 1.0)
    motion.setAngles("LKneePitch",0.800258815289,0.1)
    #motion.setAngles("LAnklePitch",-1.18943989277,0.1)
    motion.setAngles("RKneePitch",0.800258815289,0.1)
    #motion.setAngles("RAnklePitch",-1.18943989277,0.1)






    