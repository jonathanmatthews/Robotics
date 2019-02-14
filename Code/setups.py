
# from sys import path
# if setup_mode == 'Testing':
#     print "Starting test mode, will run data through algorithm"
#     path.insert(0, "Training_functions")
#     from naoqi import ALProxy
#     encoders_available = False
# elif setup_mode == 'Developing':
#     print "Using developer mode, encoders will return fake values"
#     path.insert(0, "Training_functions")
#     from naoqi import ALProxy
#     import BigEncoder
#     import SmallEncoders
#     encoders_available = True
#     print "Fake encoders connected"
# elif setup_mode == 'Real':
#     print "Using real mode, connecting encoders and robot"
#     path.insert(0, "hidlibs")  # Insert encoder path.
#     from pynaoqi.naoqi import ALProxy
#     import top_encoder.encoder_functions as BigEncoder
#     import bottom_encoder.hingeencoder as SmallEncoders
#     encoders_available = True
#     print "Encoders connected"
# elif setup_mode == 'Robot_no_encoders':
#     print "Robot no encoders mode, connecting to robot, encoders return fake values"
#     path.insert(0, "hidlibs")  # Insert encoder path.
#     from pynaoqi.naoqi import ALProxy
#     path.insert(0, "Training_functions")
#     import BigEncoder
#     import SmallEncoders
#     encoders_available = True
# elif setup_mode == "Encoders_no_robot":
#     print "Encoders no robot mode, connecting to encoders, robot will return fake values"
#     path.insert(0, "hidlibs")
#     import top_encoder.encoder_functions as BigEncoder
#     import bottom_encoder.hingeencoder as SmallEncoders
#     encoders_available = True
#     path.insert(0, "Training_functions")
#     from naoqi import ALProxy
# return encoders_available

def imports(robot, encoders):
    if robot:
        path.insert(0, "hidlibs")  # Insert encoder path.
       from pynaoqi.naoqi import ALProxy
    else:
        path.insert(0, "Training_functions")
        from naoqi import ALProxy
    if encoders:
        path.insert(0, "hidlibs")  # Insert encoder path.
        import top_encoder.encoder_functions as BigEncoder
       import bottom_encoder.hingeencoder as SmallEncoders
    else:
        path.insert(0, "Training_functions")
        import BigEncoder
        import SmallEncoders
    return encoders_available = encoders
