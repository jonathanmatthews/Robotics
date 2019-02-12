from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "169.254.61.216", 9559)

speech = raw_input("What should i say? ")
tts.say(speech)
