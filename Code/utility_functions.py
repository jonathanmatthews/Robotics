from numpy import sin, cos, pi
import numpy
from os import listdir
from collections import OrderedDict
import datetime

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


def read_file(filename):
    """
    Reads old data
    """
    data_type = current_data_types()

    # Data will be added to this with time
    all_data = numpy.empty((0, ), dtype=data_type)

    with open(filename, 'r') as f:
        file_data = f.read().split('\n')
        lines = [line.split(',') for line in file_data][:-1]
        for line in lines:
            all_data = numpy.append(all_data, numpy.array(
                [tuple(line)], dtype=data_type), axis=0)
        return all_data


def convert_read_numpy(data):
    data_type = current_data_types()
    # Data will be added to this with time
    all_data = numpy.empty((0, ), dtype=data_type)

    for i in xrange(len(data)):
        row = list(data[i])
        all_data = numpy.append(all_data, numpy.array(
            [tuple(row)], dtype=data_type), axis=0)
    return all_data


def current_data_types():
    return [('time', 'f4'), ('event', 'i4'), ('ax', 'f4'), ('ay', 'f4'), ('az', 'f4'), ('gx', 'f4'), ('gy', 'f4'),
            ('gz', 'f4'), ('se0', 'f4'), ('se1', 'f4'), ('se2',
                                                         'f4'), ('se3', 'f4'), ('be', 'f4'), ('av', 'f4'),
            ('cmx', 'f4'), ('cmy', 'f4'), ('pos', '|S10')]


def get_latest_file(current_dir):
    if current_dir == 'Code':
        output_directory = 'Output_data/'
    else:
        output_directory = '../Output_data/'
    dates = [datetime.datetime.strptime(ts, "%d-%m-%Y %H:%M:%S") for ts in listdir(output_directory)]
    dates.sort()
    latest = dates[-1]
    latest = datetime.datetime.strftime(latest, "%d-%m-%Y %H:%M:%S")
    return latest, output_directory


def convert_list_dict(current_values):
    """
    Converts list of values into a dictionary with keys of names current_data_types(), this way data
    can be accessed via values['time'] etc
    current_values: list of values with same length as current_data_types()
    """

    data_types = current_data_types()
    if len(current_values) != len(data_types):
        raise ValueError('Length of values not equal to data types length')
    values = OrderedDict()
    data_names = [key_pair[0] for key_pair in data_types]
    for i, name in enumerate(data_names):
        values[name] = current_values[i]
    return values
