from numpy import sin, cos, pi


def flatten(values):
    final_list = []
    for list_value in values:
        if isinstance(list_value, list):
            [final_list.append(value) for value in list_value]
        else:
            final_list.append(list_value)
    return final_list


def change_stiffness(stiffness, part):
    if stiffness in ['stiffen', 'Stiffen', 'stiff', 'Stiff', 'stif', 'Stiff', 'STIFF']:
        motion.setStiffnesses(part, 1.0)
        return 'Stiffening'
    else:
        motion.setStiffnesses(part, 0.0)
        return 'Loosening'


def centre_of_mass(posture, angle1, angle2, angle3):
    '''Returns the centre of mass relative to the big encoder.'''
    L1 = 1.5  # length of pendulum 1 in m
    L2 = 0.12  # length of pendulum 2 in m
    L3 = 0.20  # length of pendulum 3 in m
    a1 = angle1 * pi/180
    a2 = angle2 * pi/180
    a3 = angle3 * pi/180
    x_seat = L3 * sin(a1 + a2 + a3) + L2 * sin(a1 + a2) + L1 * sin(a1)
    y_seat = L3 * cos(a1 + a2 + a3) + L2 * cos(a1 + a2) + L1 * cos(a1)
    if posture == "seated":
        x_com = x_seat + 0.00065
        y_com = y_seat + 0.1166
    elif posture == "extended":
        x_com = x_seat + 0.0183
        y_com = y_seat + 0.1494
    else:
        raise ValueError("Position not found")
    return x_com, y_com