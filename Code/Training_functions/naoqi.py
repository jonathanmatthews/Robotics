"""
Contains class that mocks how naoqi connects to robot etc, then interface
can run away from robot if this is imported as substitute for naoqi.

Contains:
    ALProxy
"""


class ALProxy():
    def __init__(self, name, ip, port):
        pass

    def say(self, word):
        print 'NAO: ', word

    def getData(self, item):
        return 1

    def setStiffness(self, parts, stiffness):
        pass

    def setStiffnesses(self, parts, speed):
        pass

    def setAngles(self, names, angles, speed):
        pass
