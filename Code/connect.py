from naoqi import ALProxy


def router_or_you(setup='router', port=9559):
    """
    Returns ip address and port for all possible setups
    """
    if setup == 'router':
        return "192.168.1.3", 9559
    else:
        return "192.168.1.2", 9559


def check_connection():
    """
    Connects
    """
    ip_port = router_or_you('router')
    try:
        tts = ALProxy("ALTextToSpeech", *ip_port)
        tts.say("Connected")
    except BaseException:
        print('Error connecting')


if __name__ == '__main__':
    check_connection()
