from pynaoqi.naoqi import *
import sys
sys.path.insert(0, 'hidlibs')
# print dir(pynaoqi)


tts = ALProxy("ALTextToSpeech", "192.168.1.3", 9559)

speech = raw_input("What should i say? ")
tts.say(speech)
