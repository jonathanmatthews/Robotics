# python2.7


from naoqi import ALProxy

class Robot:
  def __init__(self, ip="127.0.0.1", port=9559):
    
    proxy = ALProxy("connection manager", ip, port)
    print("Network state: " + proxy.state())