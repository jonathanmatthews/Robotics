import matplotlib.pyplot as plt
from sys import path
path.insert(0, '..')
from utility_functions import get_latest_file, read_file
from graph_functions import *
from numpy.fft import fft
from scipy.signal import butter, lfilter, freqz

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)
plt.sca(ax)

filename, output_data_directory = get_latest_file('Analysis', test=False)
files = ['Accelerometer Data', 'Accelerometer Data No Movement']
# files = ['Accelerometer Data']
# files = ['Accelerometer Data No Movement']

def decompose_frequencies(time, values):
    sp = fft(values)
    freq = np.fft.fftfreq(time.shape[-1], d=dt)
    print freq
    return freq, sp

def signal_creator(frequencies, components, t):
    output = 0
    for (frequency, component) in zip(frequencies, components):
        output += component * np.sin(2 * np.pi * frequency * t)
    return output
for file_ in files:
    angles = read_file(output_data_directory + file_)

    # Extract data
    t = angles['time']
    be = angles['be']
    dt = np.mean(np.diff(t))

    # plt.title('Difference between cycle times')
    # plt.hist(dt, label='Distribution of sampling times', bins=100)
    # plt.xlabel('Cycle length (s)')
    # plt.ylabel('Relative amount of cycles with that length')
    # plt.show()

    accz = angles['az']

    # decompose_columns = ['be', 'az']
    decompose_columns = ['ax']

    for column in decompose_columns:
        plt.plot(frequencies, components.real, label='{} Real parts, file: {}'.format(column, file_))
        # plt.plot(frequencies, components.imag, label='{} Imaginary parts, file: {}'.format(column, file_))


# plt.plot(t, 100*(angles['az']+9.81), label='Accelerometer Data')
plt.title("Decomposition of frequencies,\ntaken from data in '{}'".format(file_))
plt.xlim([0, max(frequencies)])
plt.xlabel('Frequencies (Hz)')
plt.legend(loc='best')
plt.show()