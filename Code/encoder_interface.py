# python2.7
"""
A module containing class that connects to encoders and returns data.

Contains class:
    Encoders
"""


class Encoders():
    """
    Class that connects to encoders to return values, will either be fake encoders that always return 1
    or real encoders depending on the setup used in interface.py.
    """

    def __init__(self, BigEncoder, SmallEncoders):
        # BigEncoder, SmallEncoders will either be the real functions or a set of fake functions returning
        # 1 dependent on setup
        # They are imported in interface so storing retains access of them
        self.SmallEncoders = SmallEncoders
        self.BigEncoder = BigEncoder
        # Set current angle to zero point
        self.calibrate()

    def calibrate(self):
        """
        Set current angle to 0 degrees.
        """
        self.SmallEncoders.calibrate()
        self.BigEncoder.calibrate()

    def get_small_encoders(self):
        """
        Return the angles recorded by the small hinge encoders, at the base of the swing, at the time of calling.
        """

        encoder0 = self.SmallEncoders.getAngle0()
        encoder1 = self.SmallEncoders.getAngle1()
        encoder2 = self.SmallEncoders.getAngle2()
        encoder3 = self.SmallEncoders.getAngle3()

        # list of lists easier to flatten than normal tuple that would be
        # returned
        return [encoder0, encoder1, encoder2, encoder3]

    def get_big_encoder(self):
        """
        Returns the numerical value read from the large encoder at the top of the swing.
        """

        return self.BigEncoder.getAngle()
