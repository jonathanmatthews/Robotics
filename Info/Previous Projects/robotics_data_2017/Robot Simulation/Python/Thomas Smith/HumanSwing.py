#by Thomas Smith
#made by Thomas Smith 2017
import time
import SwingProxy
from naoqi import ALProxy

def test():
    robotIP = "127.0.0.1"
    #ip of the robot
    mProxy = ALProxy("ALMotion",robotIP,9559)
    file1 = open("SKnees1.txt","r")
    #opens the file with the list of angles for the knee
    file2 = open("SSholders1.txt","r")
    start = time.time()
    y1 = file1.readline()
    #reads a line from the file
    y2 = file2.readline()
    Y1 = y1.rstrip('\n')
    #strips all spaces, tabs and returns
    Y2 = y2.rstrip('\n')
    Yy1 = float(Y1)
     #converst the string into a float
    Yy2 = float(Y2)
    mProxy.setAngles("RHipPitch",-Yy2,0.5)
    #move the hip to minus the angle it reads from file2
    mProxy.setAngles("LHipPitch",-Yy2,0.5)
    mProxy.setAngles("RKneePitch",Yy1,0.5)
    #moves the knee to the angle read from file1
    mProxy.setAngles("LKneePitch",Yy1,0.5)
    mProxy.setStiffnesses("Body", 1.0)
    end = time.time()
    print end - start

def humanswing():
    #this will make the robot swing from sitting from a displaced position
    robotIP = "127.0.0.1"
    #ip of the robot
    mProxy = ALProxy("ALMotion",robotIP,9559)
    #proxy to ALMotion
    file1 = open("SKnees1.txt","r")
    #opens the file with the list of angles for the knee
    file2 = open("SSholders1.txt","r")
    #opens the file with the list of angles fro the sholders
    x = 12
    t = 0.0333333333333333
    #t = time period each frame of the original video
    p = 2.647571
    #p = period of the swinging in the video
    np = 3.27
    #np = natural period of the swing
    T = (np/p)*(t)
    #T = wait time between each frame to get the period to be the natural period
    mProxy.setStiffnesses("Body", 1.0)
    #stiffens the robot
    while x < 613:
        y1 = file1.readline()
        #reads a line from the file
        y2 = file2.readline()
        Y1 = y1.rstrip('\n')
        #strips all spaces, tabs and returns
        Y2 = y2.rstrip('\n')
        Yy1 = float(Y1)
        #converst the string into a float
        Yy2 = float(Y2)
        mProxy.setAngles("RHipPitch",-Yy2,0.5)
        #move the hip to minus the angle it reads from file2
        mProxy.setAngles("LHipPitch",-Yy2,0.5)
        mProxy.setAngles("RKneePitch",Yy1,0.5)
        #moves the knee to the angle read from file1
        mProxy.setAngles("LKneePitch",Yy1,0.5)
        time.sleep(T/2-0.0039999)
        #waits T/2
        x = x+1
        #once this loop has done it has read every angle from the file
        #need a loop that will go forever
    Y=1
    print "start"
    while Y < 2:
        mProxy.setStiffnesses("Body", 1.0)
        #this loop will go on forever
        X = 12
        file3 = open("knees1repeat.txt","r")
        #these files are both 70 frames long which covers a full osilation 
        file4 = open("sholders1repeat.txt","r")        
        while X < 82:
            x1 = file3.readline()
            x2 = file4.readline()
            X1 = x1.rstrip('\n')
            X2 = x2.rstrip('\n')
            Xx1 = float(X1)
            Xx2 = float(X2)
            mProxy.setAngles("RHipPitch",-Xx2,0.7)
            mProxy.setAngles("LHipPitch",-Xx2,0.7)
            mProxy.setAngles("RKneePitch",Xx1,0.5)
            mProxy.setAngles("LKneePitch",Xx1,0.5)
            time.sleep(0.03771-0.0039999)
            X = X+1
        file3.close()
        #need to close to the files to read from the begining again
        file4.close()
        print "close"

def humanstand():
    robotIP = "127.0.0.1"
    mProxy = ALProxy("ALMotion",robotIP,9559)
    file1 = open("standing.txt","r")
    x = 12
    t = 0.033333333333
    p = 1.95
    np = 3.27
    T = (np/p)*t
    mProxy.setStiffnesses("Body", 1.0)
    while x < 500:
        y1 = file1.readline()
        Y1 = y1.rstrip('\n')
        Yy1 = float(Y1)
        mProxy.setAngles("RHipPitch",-(Yy1/2),0.5)
        mProxy.setAngles("LHipPitch",-(Yy1/2),0.5)
        mProxy.setAngles("RKneePitch",Yy1,0.5)
        mProxy.setAngles("LKneePitch",Yy1,0.5)
        mProxy.setAngles("LAnklePitch",-(Yy1/2),0.5)
        mProxy.setAngles("RAnklePitch",-(Yy1/2),0.5)
        time.sleep(T/2)
        x = x+1
    Y = 1
    while Y < 2:
        X = 12
        file3 = open("Standingcon.txt","r")        
        while X < 72:
            x1 = file3.readline()
            X1 = x1.rstrip('\n')
            Xx1 = float(X1)
            mProxy.setAngles("RHipPitch",-(Xx1/2),0.7)
            mProxy.setAngles("LHipPitch",-(Xx1/2),0.7)
            mProxy.setAngles("RKneePitch",Xx1,0.5)
            mProxy.setAngles("LKneePitch",Xx1,0.5)
            mProxy.setAngles("LAnklePitch",-(Xx1/2),0.5)
            mProxy.setAngles("RAnklePitch",-(Xx1/2),0.5)
            time.sleep(0.0545/2)
            X = X+1
        file3.close()

def humanswingeq():
    robotIP = "127.0.0.1"
    mProxy = ALProxy("ALMotion",robotIP,9559)
    file1 = open("SRKnee4.txt","r")
    file2 = open("SRSholders4.txt","r")
    x = 12
    t = 0.04
    p = 2.44
    np = 3.27
    T = (np/p)*t
    mProxy.setStiffnesses("Body", 1.0)
    while x < 873:
        y1 = file1.readline(x)
        y2 = file2.readline(x)
        Y1 = y1.rstrip('\n')
        Y2 = y2.rstrip('\n')
        Yy1 = float(Y1)
        Yy2 = float(Y2)
        mProxy.setAngles("RHipPitch",-Yy2,0.5)
        mProxy.setAngles("LHipPitch",-Yy2,0.5)
        mProxy.setAngles("RKneePitch",Yy1,0.5)
        mProxy.setAngles("LKneePitch",Yy1,0.5)
        time.sleep(T/2)
        x = x+1
    Y=1
    while Y < 2:
        X = 12
        file3 = open("knees1repeat.txt","r")
        file4 = open("sholders1repeat.txt","r")        
        while X < 82:
            x1 = file3.readline()
            x2 = file4.readline()
            X1 = x1.rstrip('\n')
            X2 = x2.rstrip('\n')
            Xx1 = float(X1)
            Xx2 = float(X2)
            mProxy.setAngles("RHipPitch",-Xx2,0.7)
            mProxy.setAngles("LHipPitch",-Xx2,0.7)
            mProxy.setAngles("RKneePitch",Xx1,0.5)
            mProxy.setAngles("LKneePitch",Xx1,0.5)
            time.sleep(0.03771-0.0039999)
            X = X+1
        file3.close()
        file4.close()

