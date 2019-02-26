def algorithm(self, *args):
    """
    Defines how robot moves with swinging.
    Can collect old data via:
    print self.all_data
    Can move to new position via:
    self.set_posture('extended')
    pos will be name of current position
    """
    pos, time, ax, ay, az, gx, gy, gz, le0, le1, le2, le3, b_encoder = args
    self.set_posture("seated")
    print time, pos
