# python2.7
"""
Author: Jonathan Matthews.

A modules containing a class with which to access data about the robot and control it.

Contains class:
  Robot

Requires:
  naoqi
  hingeencoder
  encoder_functions
"""

from sys import path
from naoqi import ALProxy

try:
  path.insert(0, "path/to/encoder_files") # Insert encoder path.
  import hingeencoder as LittleEncoders
  import encoder_functions as BigEncoder
  encoders_available = True
  
except ImportError:
  print("Error: unable to load encoder functions, encoder data will be unavailable")
  encoders_available = False


class Robot:
  """
  Defines the class to access the robot, essentially functioning as an abstraction of the naoqi  and encoder APIs.
  """
  
  def __init__(self, ip="127.0.0.1", port=9559, initial_position="Stand"):
    """
    Sets up the connection to the robot and sets initial posture. Also calibrates encoders to zero, if available.
    Requires arguments:
    
    ip : string, contains the IPv4 address of the robot to connect to.
    port : int, contains the port number through which to access the robot.
    """
    
    # Set up connection manager.
    self.connection = ALProxy("ALConnectionManager", ip, port)
    print("Network state: " + connection.state())
    
    # Set up proxies to robot.
    self.motion = ALProxy("ALMotion", ip, port)
    self.posture = ALProxy("ALRobotPosture", ip, port)
    self.memory = ALProxy("ALMemory", ip, port)
    
    # Set up encoders, if available.
    if encoders_available:
      LittleEncoders.calibrate()
      BigEncoder.calibrate_zero()
    
    
    self.posture.goToPosture(initial_position, 1.0) # Set initial position.
  
  def get_gyro(self):
    """
    Obtain the current gyroscope data. Returns a tuple containing the (x, y, z) gyroscope data,
    in rad/s.
    """
    
    x_data = self.memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value")
    y_data = self.memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value")
    z_data = self.memory.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value") # Might not be available.
    
    return x_data, y_data, z_data
  
  def get_acc(self):
    """
    Obtain the current accelerometer data. Returns a tuple containing the (x, y, z) acceleromenter data,
    in m/s.
    """
    
    x_data = self.memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerX/Sensor/Value")
    y_data = self.memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerY/Sensor/Value")
    z_data = self.memory.getData("Device/SubDeviceList/InertialSensor/AccelerometerZ/Sensor/Value")
    
    return x_data, y_data, z_data
  
  @staticmethod
  def get_little_encoders():
    """
    Return the angles recorded by the small hinge encoders, at the base of the sqing, at the time of calling.
    If encoders are not available, will return None *without* producing an error.
    Returns a tuple, where the index of each value is the same as numbered in the source file from previous years.
    """
    
    if encoders_available:
      encoder0 = LittleEncoders.getAngle0()
      encoder1 = LittleEncoders.getAngle1()
      encoder2 = LittleEncoders.getAngle2()
      encoder3 = LittleEncoders.getAngle3()
      
      return encoder0, encoder1, encoder2, encoder3
  
  @staticmethod
  def get_big_encoder():
    """
    Returns the numerical value read from the large encoder at the top of the swing, if available. Else returns None,
    *without* producing an error.
    """
    
    if encoders_available:
      return BigEncoder.get_angle()
  
      
  
  
  
  
  
  
  
  