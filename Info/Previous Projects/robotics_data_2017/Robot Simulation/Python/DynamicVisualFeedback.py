#By Elise Dixon 23/03/17
#Swinging from visual feedback, should be released from an initial displacement

import time
import SwingAPI2 as SwingAPI
import sys
sys.path.insert(0, "/home/demo/naoqi/oldnaoqi/pynaoqi-python-2.7-naoqi-1.14-linux64")
from naoqi import ALProxy
import encoder_functions as encoder
IP = "192.168.1.3"  # Replace here with your NaoQi's IP address.
PORT = 9559
f=open('VisionOutputTest1.txt','w')
# Create a proxy to ALLandMarkDetection
try:
  landMarkProxy = ALProxy("ALLandMarkDetection", IP, PORT)
except Exception, e:
  print "Error when creating landmark detection proxy:"
  print str(e)
  exit(1)
# Subscribe to the ALLandMarkDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 50
landMarkProxy.subscribe("Test_LandMark", period, 0.0 )
# ALMemory variable where the ALLandMarkdetection modules
# outputs its results
memValue = "LandmarkDetected"
hipValue="Device/SubDeviceList/RHipPitch/Position/Sensor/Value"
# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
  motionProxy = ALProxy("ALMotion", IP, PORT)
  tts = ALProxy("ALTextToSpeech", IP, PORT)

except Exception, e:
  print "Error when creating proxies:"
  print str(e)
  exit(1)
ExpectedLandmarkID1=80
ExpectedLandmarkID2=108
#initialise position
SwingAPI.position2Dynamic(motionProxy,0.2)
initPeriod=2.561
period=initPeriod
wait=0
wait=input("Ya ready to swang?? ")
f = open("PositionSwingDynamic3fixed.txt","w")
if wait == 1:
  # Check whether we got a valid output.
  beta1=0
  dbeta1=0
  start=0
  count=1
  d2beta=0
  forward=1
  delay=0.3
  offset=0.15
  forward=0
  n=1
  skip=True
  periodStart=time.time()
  while period==initPeriod:
    val = memoryProxy.getData(memValue)
    if(val and isinstance(val, list) and len(val) >= 2):
        timeStamp = val[0]
        markInfoArray = val[1]        
        try:
            #print('Got past the try')
          # Browse the markInfoArray to get info on each detected mark.
            for markInfo in markInfoArray:
                markExtraInfo = markInfo[1]  
                if markExtraInfo[0]==ExpectedLandmarkID1:
                    # First Field = Shape info.
                    markShapeInfo = markInfo[0]              
                    # Second Field = Extra info (ie, mark ID).
                    dbeta1=beta1-markShapeInfo[2]
                    print dbeta1
            if dbeta1>0 and forward==0:
                if skip==False:
                    start = time.time()
                    toMove = True
                    #print('dbeta<0')
                    period=time.time()-periodStart
                    periodStart = start
                    print('period calculated as ',period)
                    forward=1
                skip=False
            if dbeta1<0 and forward==1:
                forward=0


        except Exception, e:
          print "Naomarks detected, but it seems getData is invalid. ALValue ="
          #print val
          print "Error msg %s" % (str(e))
    else:
      print "No landmark detected"
 
     
  toMove1=False
  toMove2=False
  t0=time.time()
  Pos2time=t0
  skip=True
  fail=False
  done=True
  wait=1
  first=True          
  while True:
    hipval = memoryProxy.getData(hipValue)
    val = memoryProxy.getData(memValue)
        
    if(val and isinstance(val, list) and len(val) >= 2):
        timeStamp = val[0]
        markInfoArray = val[1]
        try:

          # Browse the markInfoArray to get info on each detected mark.
            for markInfo in markInfoArray:
                markExtraInfo = markInfo[1]  
                if markExtraInfo[0]==ExpectedLandmarkID1:                   
                    # First Field = Shape info.
                    markShapeInfo = markInfo[0]              
                    # Second Field = Extra info (ie, mark ID).                    
                    dbeta1=beta1-markShapeInfo[2]
                    beta1=markShapeInfo[2]
                    #print dbeta1
                   # print beta1
            if dbeta1<0 and done and hipval<-0.95: #if he's in the expected position
                if forward==1 or beta1>0: #goes through this loop when it just started moving backwards
                    lastperiod=period
                    start = time.time()           
                    rawperiod=time.time()-periodStart                    
                    print("rawperiod is",rawperiod)
                    if rawperiod>(wait+1)*2.5:
                        period=rawperiod/(wait+1)
                        print('did this')
                        toMove1=True
                        done=False
                        if first:
                            theChosenPeriod=period
                            first=False  
                    if rawperiod>2 and rawperiod<3.5: 
                        period=rawperiod
                        toMove1=True
                        done=False
                        if first:
                            theChosenPeriod=period
                            first=False 
                    if period>3.5:
                        period=lastperiod
                    periodStart = start
                    periodNumber= (time.time()-t0)/2.561        
                    forward=0
                    fail=False                                  
                   
            if dbeta1>0 or beta1==0:
                forward=1

        except Exception, e:
          print "Naomarks detected, but it seems getData is invalid. ALValue ="
          #print val
          print "Error msg %s" % (str(e))
    else:
      beta1=0
      dbeta1=0
    if period>2 and period<3.5 and not done:
        if abs(period-theChosenPeriod)<0.2 and period!=theChosenPeriod:
            wait=wait+1
            print("added to wait cus thingy was ",abs(period-theChosenPeriod) )
        if abs(period-theChosenPeriod)>=0.2 :
            wait=1
            print("reset wait cus thingy was ",abs(period-theChosenPeriod) )
        theChosenPeriod=period
        n=1

        print("wait =", wait)
        while n<wait+1:
            done=False
            if (time.time()-start) > n*(period)-delay-offset and toMove1 and not fail:
                SwingAPI.position1Dynamic(motionProxy,0.75)
                print("LeanBack at time", ((time.time()-start)/period))
                toMove2=True
                toMove1=False
                Pos2time=time.time()
                skip=False
                n=n+0.5
            if (time.time()-start) > (n)*(period)-delay-offset and toMove2 and not fail: 
            #Decide which position to switch to
                SwingAPI.position2Dynamic(motionProxy,0.75)
                print("LeanFwd at time", ((time.time()-start)/period))
                toMove2=False
                toMove1=True
                skip=False
                n=n+0.5
            if wait>8:
                wait=8
            hipval = memoryProxy.getData(hipValue)
            f.write(str(time.time()-t0))
            f.write(";")
            f.write(str(encoder.get_angle()))
            f.write(";")
            f.write(str(hipval))
            f.write(";")
            f.write(str(beta1))
            f.write(";")
            f.write(str(dbeta1))
            f.write("\n")
        done=True
    else:
        hipval = memoryProxy.getData(hipValue)
        f.write(str(time.time()-t0))
        f.write(";")
        f.write(str(encoder.get_angle()))
        f.write(";")
        f.write(str(hipval))
        f.write(";")
        f.write(str(beta1))
        f.write(";")
        f.write(str(dbeta1))
        f.write("\n")
  
  
      
 
      
