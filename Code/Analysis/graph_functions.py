import matplotlib.pyplot as plt
import numpy
import numpy as np
from functools import reduce


position_numbers = {
    'extended': 1,
    'seated': -1,
    1.0: 'extended',
    -1.0: 'seated',
    'folded': 2.0,
    'unfolded': -2.0,
    2.0: 'folded',
    -2.0: 'unfolded',
    0.0: ''
}

def format_graph(axis):
    """
    Works out if axis is a list of axis' or not, and if so individually formats each one
    """
    if isinstance(axis, numpy.ndarray):
        return [format_axis(ax) for ax in axis.flat]
    else:
        return format_axis(axis)


def format_axis(ax):
    """
    This formats an axis according to the style guidelines set below
    """
    plt.sca(ax)
    # ax.set_facecolor('#eeeeee')
    plt.rcParams.update({'axes.titlesize': 18,
                         'legend.fontsize': 14,
                         'font.serif': 'Computer Modern Roman', })
    ax.yaxis.label.set_size(18)
    ax.xaxis.label.set_size(18)
    ax.tick_params(axis='both', labelsize=15)


    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    return ax
    
def shade_background_based_on_algorithm(time, algorithm):
    """
    Shades axis darker and darker grey whenever algorithm changes
    ax: singular matplotlib axis to be shaded
    time: list of recorded times
    algorithm: list of corresponding algorithm at each 
    """
    # where algorithm changes and difference in indexes between current and next algorithm
    algorithm_change_indexes = np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))
    algorithm_change_diff = np.diff(algorithm_change_indexes)

    # for each change in algorithm shade background slightly darker
    for i, index in enumerate(algorithm_change_indexes[:-1]):
        plt.axvspan(time[index], time[index + algorithm_change_diff[i]], alpha = (i+1) * 0.15, color='grey', label='{}'.format(algorithm[index+1]))
    return algorithm_change_indexes

def algorithm_change_indexes(algorithm):
    return np.append(np.where(algorithm[:-1] != algorithm[1:])[0], np.array(len(algorithm) - 1))

def combine_multiple_legends(axes, custom_location='best'):
    lines = []
    labels = []
    for axis in axes:
        linesax, labelsax = axis.get_legend_handles_labels()
        lines.append(linesax)
        labels.append(labelsax)
    plt.legend(reduce((lambda x, y: x + y), lines),  reduce((lambda x, y: x + y), labels), loc=custom_location, framealpha=1.0)
    
def times_and_values_maxima(time, values, start_time=0.0, end_time=10000000):
    """
    Returns times of maximas and values at the time
    time: list of times
    values: values at those corresponding times, can be any list doesn't have to be big encoder value
    """
    end_index = np.where(time <= end_time)[0][-1]
    start_index = np.where(start_time <= time)[0][0]
    time = time[start_index:end_index+1]
    values = values[start_index:end_index+1]

    # time, values = np.where(start_time <= time <= end_time, time, values)

    # these are the maxima of the graphs, will be used for fitting to look at trend
    max_index = (np.diff(np.sign(np.diff(values))) < 0).nonzero()[0] + 1
    time_max = time[max_index]
    value_max = values[max_index]
    return time_max, value_max

def add_named_position_plot(time, positions):
    """
    This adds the position over time, and format the axis correctly with name, want a new axis over the top
    of old one before doing this, aka ax2 = ax.twinx() then plt.sca(ax2), then add_named_position_plot(time, positions)
    positions: list of named positions
    """
    position_number = [position_numbers[i] for i in positions]
    common_keys = list(set(positions).intersection(position_numbers.keys()))
    plt.ylabel('Named position')
    y_tick_values = np.linspace(min(position_number), max(position_number), len(common_keys) + 1)
    y_tick_labels = [position_numbers[i] for i in y_tick_values]
    plt.yticks(y_tick_values, y_tick_labels)
    plt.yticks(rotation=-45)

    position_number = [position_numbers[i] for i in positions]
    plt.plot(time, position_number, color='r', label='Position of Nao', linewidth=0.5)