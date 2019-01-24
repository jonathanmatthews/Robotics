import time
import SwingAPI
import SwingProxy
from naoqi import ALProxy

#   Author: Harry Withers
#   Date:   02/03/2017
#
#   This file uses the position of the swing to calculate when
#   to change position next. It does this by finding when the
#   robot is at the bottom of its swing (theta=0) and counts out
#   a quarter of a period from that point.

def Main():
    #Open file for data
    f = open("PositionSwing.txt","w")

    #Address of Robot and Swing
    IP = "127.0.0.1"
    ROBOT_PORT = 9559
    SWING_PORT = 5005
    #Robot and Swing proxies
    motionProxy = ALProxy("ALMotion", IP, ROBOT_PORT)
    #Change this line to connect to real angle encoder
    swingProxy = SwingProxy.SwingProxy(IP, SWING_PORT)

    #Natural period of the virtual swing
    period = 3.27

    #Natural period of the real swing
    #period = 2.561

    #First previous angle
    prevAngle = 0
    #Initial start time for swinging
    start = 0
    #Does not need to move yet
    toMove = False
    #Start time of simulation
    startSim = time.time()

    #Loop
    while True:
        #Offset for if 0 is not centre of swing
        offset = 0
        #Get the next angle
        angle = swingProxy.get_angle()+offset
        #If negative then just passed bottom of swing
        if (prevAngle*angle) < 0:
            #Set time passed bottom of swing
            start = time.time()
            toMove = True
        #Change position at estimated top of swing and if not in correct pos
        if (time.time()-start) > (period/4) and toMove:
            #Decide which position to switch to
            if angle > 0:
                SwingAPI.position1Dynamic(motionProxy,0.75)
                toMove = False
            elif angle < 0:
                SwingAPI.position2Dynamic(motionProxy,0.75)
                toMove = False
        #Set prevAngle for next iteration
        prevAngle = angle
        # Find time elapsed since start of simulation
        timeElaps = time.time() - startSim
        #Stringify time elapsed and angle
        stimeElaps = str(timeElaps)
        sangle = str(angle)
        # print values to file with tabs and new line
        f.write(stimeElaps)
        f.write('\t\t')
        f.write(sangle)
        f.write('\n')
Main()