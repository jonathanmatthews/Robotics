#made by Thomas Smith 2017
import SwingProxy
import SwingAPI
import time
from naoqi import ALProxy

def Main():
    #Get Swing proxy
    robotIP = "127.0.0.1"
    mProxy = ALProxy("ALMotion",robotIP,9559)
    
    IP = "127.0.0.1"
    SWING_PORT = 5005
    swingProxy = SwingProxy.SwingProxy(IP,5005)
    f = open("Swing.txt","w")
    start = time.time()
    file1 = open("SKnees1.txt","r")
    file2 = open("SSholders1.txt","r")
    x = 12
    t = 0.0333333333333333
    p = 2.647571
    np = 3.27
    T = (np/p)*(t)
    
    while x < 613:
        y1 = file1.readline()
        y2 = file2.readline()
        Y1 = y1.rstrip('\n')
        Y2 = y2.rstrip('\n')
        Yy1 = float(Y1)
        Yy2 = float(Y2)
        
        SwingAPI.moveLimbs(mProxy,"RHipPitch",-Yy2,0.5)
        SwingAPI.moveLimbs(mProxy,"LHipPitch",-Yy2,0.5)
        SwingAPI.moveLimbs(mProxy,"RKneePitch",Yy1,0.5)
        SwingAPI.moveLimbs(mProxy,"LKneePitch",Yy1,0.5)
        
        timeElaps = time.time()-start
        angle = swingProxy.get_angle()
        stimeElaps = str(timeElaps)
        sangle = str(angle)
        #print values to file with tabs
        f.write(stimeElaps)
        f.write('\t\t')
        f.write(sangle)
        f.write('\n')
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
            print Xx1
            
            SwingAPI.moveLimbs(mProxy,"RLeg","RHipPitch",-Yy2,0.5,0)
            SwingAPI.moveLimbs(mProxy,"LLeg","LHipPitch",-Yy2,0.5,0)
            SwingAPI.moveLimbs(mProxy,"RLeg","RKneePitch",Yy1,0.5,0)
            SwingAPI.moveLimbs(mProxy,"LLeg","LKneePitch",Yy1,0.5,0)
            
            timeElaps = time.time()-start
            angle = swingProxy.get_angle()
            stimeElaps = str(timeElaps)
            sangle = str(angle)
            #print values to file with tabs
            f.write(stimeElaps)
            f.write('\t\t')
            f.write(sangle)
            f.write('\n')
            time.sleep(0.03771)
            X = X+1
        file3.close()
        file4.close()
    f.close()
Main()
