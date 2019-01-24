import sys
#made by Thomas Smith
import motion
import almath
import time
import math
import JointRanges
import SwingAPI
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def Kickoff():
    robotIP = "127.0.0.1"
    MemProxy = ALProxy("ALMemory", robotIP, 9559)
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.setStiffnesses("LLeg", 1.0)
    mProxy.setAngles("LHipRoll",0,0.1)
    mProxy.setAngles("LHipPitch",0,0.1)
    mProxy.setAngles("LKneePitch",1.607669,0.1)
    mProxy.setAngles("LAnklePitch",-0.677419,0.1)
    mProxy.setAngles("LAnkleRoll",0,0.1)
    mProxy.setAngles("RHipRoll",0,0.1)
    mProxy.setAngles("RHipPitch",0,0.1)
    mProxy.setAngles("RKneePitch",1.607669,0.1)
    mProxy.setAngles("RAnklePitch",-0.677419,0.1)
    mProxy.setAngles("RAnkleRoll",0,0.1)
    time.sleep(5)
    X = 0
    while X == 0:
        BothLegs(0,0,-0.01,0.01,0,0.1)
        X = MemProxy.getData("LeftBumperPressed")
        Y = MemProxy.getData("Device/SubDeviceList/RKneePitch/Position/Sensor/Value")
        if Y <= 0.6:
            X = 1
    time.sleep(5)
    BothLegs(0,0,0,-1.5,0,0.1)
    time.sleep(5)
    BothLegs(0,0,-0.7,0.4,0,0.1)
    time.sleep(2)
    BothLegs(0,0,-4,4,0,0.7)
    time.sleep(1)
    smoothPeriodic(mProxy,2.435/2,10)
        
def getAng():
    robotIP = "127.0.0.1"
    MemProxy = ALProxy("ALMemory", robotIP, 9559)
    x = MemProxy.getData("Device/SubDeviceList/LHipRoll/Position/Sensor/Value")
    y = MemProxy.getData("Device/SubDeviceList/LHipPitch/Position/Sensor/Value")
    z = MemProxy.getData("Device/SubDeviceList/RKneePitch/Position/Sensor/Value")
    X = MemProxy.getData("Device/SubDeviceList/LAnklePitch/Position/Sensor/Value")
    Y = MemProxy.getData("Device/SubDeviceList/LAnkleRoll/Position/Sensor/Value")
    xx='sholpitch'
    yy='sholroll'
    zz='elbyaw' 
    Xx='elbroll' 
    Yy='wristyaw'
    print xx, x
    print yy, y
    print zz, z
    print Xx, X
    print Yy, Y

def getready():
    robotIP= "127.0.0.1"
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.setStiffnesses("LLeg", 1.0)
    mProxy.setAngles("LKneePitch",1.30001437664,0.1)
    mProxy.setAngles("LAnklePitch",-0.299998551607,0.1)
    mProxy.setAngles("RKneePitch",1.30001437664,0.1)
    mProxy.setAngles("RAnklePitch",-0.299998551607,0.1)

def LArm( LSP, LSR, LEY, LER, LWY, LH , Speed ):
    robotIP= "127.0.0.1"
    lsp = LSP
    lsr = LSR
    ley = LEY
    ler = LER
    lwy = LWY
    lh = LH
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("LArm", 1.0)
    mProxy.changeAngles("LShoulderPitch",lsp,speed)
    mProxy.changeAngles("LShoulderRoll",lsr,speed)
    mProxy.changeAngles("LElbowYaw",ley,speed)
    mProxy.changeAngles("LElbowRoll",ler,speed)
    mProxy.changeAngles("LWristYaw",lwy,speed)
    mProxy.changeAngles("LHand",lh,speed)      

def RArm( RSP, RSR, REY, RER, RWY, RH, Speed ):
    robotIP= "127.0.0.1"
    rsp = RSP
    rsr = RSR
    rey = REY
    rer = RER
    rwy = RWY
    rh = RH
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RArm", 1.0)
    mProxy.changeAngles("RShoulderPitch",rsp,speed)
    mProxy.changeAngles("RShoulderRoll",rsr,speed)
    mProxy.changeAngles("RElbowYaw",rey,speed)
    mProxy.changeAngles("RElbowRoll",rer,speed)
    mProxy.changeAngles("RWristYaw",rwy,speed)
    mProxy.changeAngles("RHand",rh,speed)

def BothArms( SP, SR, EY, ER, WY, H, Speed):
    robotIP= "127.0.0.1"
    sp = SP
    sr = SR
    ey = EY
    er = ER
    wy = WY
    h = H
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("LArm", 1.0)
    mProxy.setStiffnesses("RArm", 1.0)
    mProxy.changeAngles("LShoulderPitch",sp,speed)
    mProxy.changeAngles("LShoulderRoll",sr,speed)
    mProxy.changeAngles("LElbowYaw",-ey,speed)
    mProxy.changeAngles("LElbowRoll",-er,speed)
    mProxy.changeAngles("LWristYaw",-wy,speed)
    mProxy.changeAngles("LHand",h,speed)
    mProxy.changeAngles("RShoulderPitch",sp,speed)
    mProxy.changeAngles("RShoulderRoll",-sr,speed)
    mProxy.changeAngles("RElbowYaw",ey,speed)
    mProxy.changeAngles("RElbowRoll",er,speed)
    mProxy.changeAngles("RWristYaw",wy,speed)
    mProxy.changeAngles("RHand",h,speed)
    
def Hips(LH,RH,Speed):
    robotIP= "127.0.0.1"
    lh = LH
    rh = RH
    speed =Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("LHipYawPitch", 1.0)
    mProxy.setStiffnesses("RHipYawPitch", 1.0)
    mProxy.changeAngles("LHipYawPitch",lh,speed)
    mProxy.changeAngles("LHipYawPitch",rh,speed)

def LLeg(LHR, LHP, LKP, LAP, LAR, Speed):
    robotIP= "127.0.0.1"
    lhr = LHR
    lhp = LHP
    lkp = LKP
    lap = LAP
    lar = LAR
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("LLeg", 1.0)
    mProxy.changeAngles("LHipRoll",lhr, speed)
    mProxy.changeAngles("LHipPitch",lhp,speed)
    mProxy.changeAngles("LKneePitch",lkp,speed)
    mProxy.changeAngles("LAnklePitch",lap,speed)
    mProxy.changeAngles("LAnkleRoll",lar,speed)

def RLeg(RHR, RHP, RKP, RAP, RAR, Speed):
    robotIP= "127.0.0.1"
    rhr = RHR
    rhp = RHP
    rkp = RKP
    rap = RAP
    rar = RAR
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.changeAngles("RHipRoll",rhr, speed)
    mProxy.changeAngles("RHipPitch",rhp,speed)
    mProxy.changeAngles("RKneePitch",rkp,speed)
    mProxy.changeAngles("RAnklePitch",rap,speed)
    mProxy.changeAngles("RAnkleRoll",rar,speed)

def BothLegs(HR, HP, KP, AP, AR, Speed):
    robotIP= "127.0.0.1"
    hr = HR
    hp = HP
    kp = KP
    ap = AP
    ar = AR
    speed = Speed
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.setStiffnesses("LLeg", 1.0)
    mProxy.changeAngles("LHipRoll",hr, speed)
    mProxy.changeAngles("LHipPitch",hp,speed)
    mProxy.changeAngles("LKneePitch",kp,speed)
    mProxy.changeAngles("LAnklePitch",ap,speed)
    mProxy.changeAngles("LAnkleRoll",ar,speed)
    mProxy.changeAngles("RHipRoll",hr, speed)
    mProxy.changeAngles("RHipPitch",hp,speed)
    mProxy.changeAngles("RKneePitch",kp,speed)
    mProxy.changeAngles("RAnklePitch",ap,speed)
    mProxy.changeAngles("RAnkleRoll",ar,speed)

def moveLimbs(motionProxy,limbs,angleNames,angles,speed,restInt):
    motionProxy.setStiffnesses(limbs,1.0)
    motionProxy.setAngles(angleNames,angles,speed)
    time.sleep(restInt)

def position1(motionProxy):
    #Limbs and angle names
    limbs=["Head","RLeg","LLeg"]
    angleNames=["HeadPitch","RHipPitch","LHipPitch","RKneePitch","LKneePitch"]
    #Angle values
    headAngle=-0.6685
    hipAngle=0.513
    kneeAngle=-0.09
    angles=[headAngle,-hipAngle,-hipAngle,kneeAngle,kneeAngle]
    #speed and rest interval
    speed=0.75
    restInt=0.001
    #Send the move request
    moveLimbs(motionProxy,limbs,angleNames,angles,speed,restInt)


def position2(motionProxy):
    #Limbs and angle names
    limbs=["Head","RLeg","LLeg"]
    angleNames=["HeadPitch","RHipPitch","LHipPitch","RKneePitch","LKneePitch"]
    #Angle values
    headAngle=0.5115
    hipAngle=0.985
    kneeAngle=1.55
    angles=[headAngle,-hipAngle,-hipAngle,kneeAngle,kneeAngle]
    #speed and rest interval
    speed=0.75
    restInt=0.001
    #Send the move request
    moveLimbs(motionProxy,limbs,angleNames,angles,speed,restInt)

def smoothPeriodic(motionProxy,period,numSwings):
    #Setup timing
    numSteps=1000
    restInt=float(period)/float(numSteps)
    high = int(numSteps*period)
    #Limb and angle setup
    limbs=["Head","RLeg","LLeg"]
    angleNames=["HeadPitch","RHipPitch","LHipPitch","RKneePitch","LKneePitch"]
    for i in range(0,numSwings):
        for j in range(0,high):
            x=j*(2*math.pi/numSteps)
            headAngle=0.59*math.sin(x/period)-0.0785
            hipAngle=0.236*math.sin(x/period)+0.749
            kneeAngle=0.82*math.sin(x/period)+0.73
            angles=[headAngle,-hipAngle,-hipAngle,kneeAngle,kneeAngle]
            SwingAPI.moveLimbs(motionProxy,limbs,angleNames,angles,0.5,restInt)

def stepPeriodic(motionProxy,period,numSwings):
    restInt=float(period)/2.0
    for x in range(0,numSwings):
        SwingAPI.moveLegs(motionProxy,LEGS_MAX,restInt)
        SwingAPI.moveLegs(motionProxy,LEGS_MIN,restInt)

def GetReady():
    robotIP= "127.0.0.1"
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.setStiffnesses("LLeg", 1.0)
    mProxy.setAngles("LKneePitch",0.800258815289,0.1)
    mProxy.setAngles("LAnklePitch",-1.18943989277,0.1)
    mProxy.setAngles("RKneePitch",0.800258815289,0.1)
    mProxy.setAngles("RAnklePitch",-1.18943989277,0.1)

def pushoff():
    robotIP= "127.0.0.1"
    mProxy = ALProxy("ALMotion", robotIP, 9559)
    mProxy.setStiffnesses("RLeg", 1.0)
    mProxy.setStiffnesses("LLeg", 1.0)
    BothLegs(0, 0, -1, 1, 0, 0.75)
          
def main(robotIP):

    robotIP="127.0.0.1"
    PORT=9559
    motionProxy=ALProxy("ALMotion",robotIP,PORT)
    #smoothPeriodic(motionProxy,1/2.435,10)
    smoothPeriodic(motionProxy,1.5,5)


    
