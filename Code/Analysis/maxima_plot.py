import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path
path.insert(0, '..')
from utility_functions import read_file, moving_average

output_data_directory = '../Output_data/'

def get_files(folder):
    files = sorted(os.listdir(folder))
    text = ["{} {}".format(i, file_) for i, file_ in enumerate(files)]
    compare = str(
        input(
            'Select all files to compare, seperate by commas: \n{}\n'.format(
                "\n".join(text))))
    # print list(compare)
    numbers = list(compare.replace(')', '').replace('(', '').split(','))
    responses = [files[int(i)] for i in numbers if int(i) <= len(files)]
    files = []

    for response in responses:
        try:
            open(folder + response).close()
            files.append(folder + response)
        except IOError: # Response is a folder.
            other = get_files(folder + response + "/")
            for i in other:
                files.append(i)
    
    return files


def get_name(location):
    """
    Get the file name from a path, eg: /home/me/file.jpg -> file.jpg
    """
    result = ""
    for i in range(len(location)):
        if location[-i] == "/":
            break

        result = location[-i] + result
    
    return result


files_to_compare = get_files(output_data_directory)



def plot_maxima_curve(filename, plot=True):
    angles = read_file(filename)
    time = angles['time']
    be = angles['be']
    algo = angles['algo']

    algo_change_indexes = shade_background_based_on_algorithm(time, algo, plot=False)

    # only take values from when algorithm is switched to increasing
    time = time[algo_change_indexes[1]:]
    be = be[algo_change_indexes[1]:]

    # there is a weird spike that goes really high, this filters that out
    time = time[be < 30]
    be = be[be < 30]
    # again something else to filter
    time = time[be > 1]
    be = be[be > 1]

    # calculate maximas after smoothing results together
    window_size = 5
    avg_be = np.array(moving_average(be, window_size=window_size))
    angle_max_index = (np.diff(np.sign(np.diff(avg_be))) < 0).nonzero()[0] + 1 + (window_size - 1)/2

    # take times and values at maximas
    time = time[angle_max_index]
    be = be[angle_max_index]

    # Some specific filtering for the rotational datafile
    if filename == '../Output_data/Rotational No Masses 400secs':
        filtered_time, filtered_be = [], []
        for time_, be_ in zip(time, be):
            # print time_, be_
            if time_ <= 165 or time_ >= 185:
                filtered_time.append(time_)
                filtered_be.append(be_)
            elif 165 < time_ < 185:
                if be_ > 8.4:
                    filtered_time.append(time_)
                    filtered_be.append(be_)
            else:
                print "Doesn't fit category", time_, be_   
        time, be = filtered_time, filtered_be


    # Remove as many weird spikes as possible
    filtered_time, filtered_be = [], []
    for time_, be_ in zip(time, be):
        if time_ <= 260 or 400 <= time_ <= 600 or time_ >= 700:
            filtered_time.append(time_)
            filtered_be.append(be_)
        elif 260 < time_ < 400:
            if be_ > 6.8:
                filtered_time.append(time_)
                filtered_be.append(be_)
        elif 600 < time_ < 700:
            if be_ > 17.5:
                filtered_time.append(time_)
                filtered_be.append(be_)
        else:
            print "Doesn't fit category", time_, be_   


    # convert to numpy arrays get some weird error without
    time, be = np.array(filtered_time), np.array(filtered_be)
    # centre them so they both start the plot at zero
    print 'Time offset for file {}: {}s'.format(filename, time[0])
    time -= time[0]


    label = get_name(each_file)[:-1]
    if label == 'Rotational No Masses 400secs':
        label = 'Quarter Period'
    if plot:
        # plot against each other
        plt.plot(time, be, label=label)
    return time, be

fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
ax = format_graph(ax)
for each_file in files_to_compare:
    time, be = plot_maxima_curve(each_file)

ax.set_facecolor('#eeeeee')
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")
plt.title('Comparison between different methods for calculating\nthe best time to kick')
# plt.title('Comparison between rotational and parametric pumping')
plt.legend(loc='best')
fig.tight_layout()
plt.show()  

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/RotationalVsParametric.eps', format='eps')
fig.savefig(
    'Figures/RotationalVsParametric.png', format='png'
)

# second plot of gradient here
fig, ax = plt.subplots(
    1, 1, figsize=(
    8, 6))
ax = format_graph(ax)
ax.set_facecolor('#eeeeee')
plt.xlabel(r"$\theta$ " + r"$(^o)$")
plt.ylabel(r"$\frac{d\theta}{dt} $" + r"$(^os^{-1})$")
# plt.title('Comparison between different recorded motions')
# plt.title('Rate of increase of angle for\nrotational and parametric pumping')
plt.title('Comparison between different methods for calculating when to kick')
for each_file in files_to_compare:
    time, be= plot_maxima_curve(each_file, plot=False)
    # smooth results then calculate gradient and plot
    avg_be = moving_average(be, 29)
    avg_time = moving_average(time, 29)
    gradient = [diff/(avg_time[i+1] - avg_time[i]) for i, diff in enumerate(np.diff(avg_be))]

    dictionary_gradient = {}
    for value, gradient_ in zip(avg_be[1:], gradient):
        round_value = round(value, 0)
        if round_value not in dictionary_gradient.keys():
            dictionary_gradient[round_value] = []
        dictionary_gradient[round_value].append(gradient_) 
    avg_grad = [np.mean(dictionary_gradient[key]) for key in dictionary_gradient.keys()]

    label = get_name(each_file)[:-1]
    if label == 'Rotational No Masses 400secs':
        label = 'Quarter Period'
    plt.scatter(dictionary_gradient.keys(), avg_grad, label=label, s=20.0)

plt.legend(loc='best')
fig.tight_layout()
plt.show()

# eps is vector graphic doesn't get worse in quality when in latex
fig.savefig(
    'Figures/RotationalVsParametricGradient.eps', format='eps')
fig.savefig(
    'Figures/RotationalVsParametricGradient.png', format='png'
)


