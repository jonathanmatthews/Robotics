import SwingProxy
import time

#   Author: Harry Withers
#   Date:   03/03/2017
#
#   This file reads the position of the swing at a time, t
#   to a text file.

def Main():
    #Get Swing proxy
    IP = "127.0.0.1"
    SWING_PORT = 5005
    swingProxy = SwingProxy.SwingProxy(IP,SWING_PORT)
    #Open file
    f = open("Swing.txt","w")
    #Count for loop and start time for time elapsed
    count = 0
    start = time.time()
    while count < 10000000:
        timeElaps = time.time()-start
        angle = swingProxy.get_angle()

        stimeElaps = str(timeElaps)
        sangle = str(angle)

        #print values to file with tabs
        f.write(stimeElaps)
        f.write('\t\t')
        f.write(sangle)
        f.write('\n')

        count += 1

    f.close()

Main()