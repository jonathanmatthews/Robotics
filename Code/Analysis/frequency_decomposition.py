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
    return freq, sp

def signal_creator(frequencies, components, t):
    output = 0
    for (frequency, component) in zip(frequencies, components):
        output += component * np.sin(2 * np.pi * frequency * t)
    return output

for i, file_ in enumerate(files):
    angles = read_file(output_data_directory + file_)

    # Extract data
    t = angles['time']
    be = angles['be']
    accz = angles['az']
    accz = accz[t > 10]
    t = t[t > 10]
    accz = accz[t < 27.5]
    t = t[t < 27.5]
    dt = np.mean(np.diff(t))

    # plt.title('Difference between cycle times')
    # plt.hist(dt, label='Distribution of sampling times', bins=100)
    # plt.xlabel('Cycle length (s)')
    # plt.ylabel('Relative amount of cycles with that length')
    # plt.show()


    # plt.plot(t, accz)
    # plt.show()

    # decompose_columns = ['be', 'az']
    decompose_columns = ['az']

    for column in decompose_columns:
        frequencies, components = decompose_frequencies(t, accz)
        components = components[frequencies > 0.1]
        frequencies = frequencies[frequencies > 0.1]
        scaling = max(abs(components))
        print i, file_
        components = abs(components)/scaling
        if i == 0:
            label = 'Changing Posture'
        if i == 1:
            label = 'Static Posture'
        plt.plot(frequencies, abs(components), zorder=1/(i+1), label=label + r'$ \times {:.2f}$'.format(1/scaling))
        # plt.plot(frequencies, components.imag, label='{} Imaginary parts, file: {}'.format(column, file_))
    # plt.show()

# plt.plot(t, 100*(angles['az']+9.81), label='Accelerometer Data')
plt.title('Fourier Transform of Z Accelerometer Data for Static and Changing Postures')
plt.xlim([0, max(frequencies)])
plt.xlabel('Frequencies (Hz)')
plt.ylabel('Relative Amplitude')
plt.legend(loc='best')
plt.show()
fig.savefig(
    'Figures/FrequencyDecomposition.eps', format='eps')