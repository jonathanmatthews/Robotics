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
    if stiffness in ['stiffen', 'Stiffen', 'stiff',
                     'Stiff', 'stif', 'Stiff', 'STIFF']:
        motion.setStiffnesses(part, 1.0)
        return 'Stiffening'
    else:
        motion.setStiffnesses(part, 0.0)
        return 'Loosening'

