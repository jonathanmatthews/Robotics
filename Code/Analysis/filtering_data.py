import matplotlib.pyplot as plt
from sys import path
path.insert(0, '..')
from utility_functions import get_latest_file, read_file
from graph_functions import *
from numpy.fft import fft
from scipy.signal import butter, lfilter, freqz

# access latest file if underneath file name is blanked out
filename, output_data_directory = get_latest_file('Analysis', test=False)
filename = 'Accelerometer Data'
# filename = 'Accelerometer Data No Movement'
angles = read_file(output_data_directory + filename)

# Extract data
t = angles['time']
be = angles['be']
position = angles['pos']
algorithm = angles['algo']
dt = np.mean(np.diff(t))

accx = angles['ax']
accy = angles['ay']
accz = angles['az']

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

ax = format_graph(ax)



def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter requirements.
order = 6
fs = 1.0/dt       # sample rate, Hz
cutoff = 0.65# desired cutoff frequency of the filter, Hz
lowcut = 0.35
highcut = 0.50

y = butter_bandpass_filter(accz, lowcut, highcut, fs, order)

# plt.plot(t, accx, 'b-', label='accx')
# plt.plot(t, accy, 'g-', label='accy')
plt.plot(t, accz, 'r-', label='accz')

plt.plot(t, be, label='Big Encoder')
# y_middle = np.mean(y[-140])
plt.plot(t, y, 'g-', linewidth=2, label='Filtered accz')

plt.title("Data in '{}'".format(filename))
plt.legend(loc='upper right')
plt.xlabel('Time [sec]')
plt.show()

