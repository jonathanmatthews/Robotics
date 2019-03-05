from naoqi import ALProxy
from positions import positions
from limb_data import values


def set_posture(name_posture, max_speed=1.0):
    posture = positions[name_posture]
    names = [values[name][0] for name in posture.keys()]
    speed = [max_speed * (values[named_part_range][5] / 1.4920799999999999)
             for named_part_range in posture.keys()]
    # Need stiffness set to 1.0 before can move
    motion.setStiffnesses(
        ["Head", "RArm", "LArm", "RLeg", "LLeg"], 1)
    # Start movement of each part
    for i, speed_value in enumerate(speed):
        motion.setAngles(
            names[i], list(
                posture.values())[i], speed_value)
    position = name_posture


tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)
motion = ALProxy("ALMotion", "127.0.0.1", 9559)
motion.setStiffnesses(["Head", "RArm", "LArm", "RLeg", "LLeg"], 1)
tts.say("Connected!")

set_posture("extended")
