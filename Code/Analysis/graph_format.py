import matplotlib.pyplot as plt
import numpy

def format_graph(axis):
    if type(axis) == numpy.ndarray:
        return [format_axis(ax) for ax in axis]
    else:
        return format_axis(axis)

def format_axis(ax):
    plt.sca(ax)
    ax.set_facecolor('#eeeeee')
    plt.rcParams.update({'axes.titlesize': 18,
                        'legend.fontsize': 14,
                        'font.serif': 'Computer Modern Roman', })
    ax.yaxis.label.set_size(16)
    ax.xaxis.label.set_size(16)

    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    return ax