import matplotlib.pyplot as plt
from sys import path
path.insert(0, '..')
from utility_functions import get_latest_file, read_file
from graph_functions import *
from numpy.fft import fft, ifft
from scipy.signal import butter, lfilter, freqz, filtfilt

def zero_maxima(min_max, time_list, values_list, time_values='time', dt=0.005):
    """
    Generalised function that calculates zero crossing point or maxima value 
    """
    n = int(6.0 / dt)
    window_number = int(0.8 / dt)
    if window_number % 2 == 0:
        window_number += 1
    if window_number == 1:
        window_number = 3
    
    avg_values_list = np.abs(moving_average(values_list[-n:], window_number))
    if min_max == 'min':
        max_index = (np.diff(sign_zero(np.diff(np.abs(avg_values_list)))) > 0).nonzero()[0] + 1 + (window_number - 1)/2
    elif min_max == 'max':
        max_index = (np.diff(sign_zero(np.diff(avg_values_list))) < 0).nonzero()[0] + 1 + (window_number - 1)/2
    elif min_max == 'either':
        max_index = (np.abs(np.diff(sign_zero(np.diff(np.abs(avg_values_list))))) > 0).nonzero()[0] + 1 + (window_number - 1)/2
    else:
        raise ValueError('Choice of min or max not provided')
    
    if time_values == 'time':
        return time_list[-n:][max_index[-1]]
    elif time_values == 'values':
        return values_list[-n:][max_index[-1]]
    elif time_values == 'both':
        return time_list[-n:][max_index[-1]], values_list[-n:][max_index[-1]]
    else:
        raise ValueError('Last maxima is not returning anything')

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

accz = accz[t < 25]
be = be[t < 25]
t = t[t < 25]

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
cutoff = 0.55# desired cutoff frequency of the filter, Hz
lowcut = 0.35
highcut = 0.50

# y = butter_bandpass_filter(accz, lowcut, highcut, fs)
y = butter_lowpass_filter(accz, cutoff, fs, order)

# plt.plot(t, accx, 'b-', label='accx')
# plt.plot(t, accy, 'g-', label='accy')
plt.plot(t, accz, 'r-', label='accz')

plt.plot(t, be, label='Big Encoder')
plt.plot(t, y, 'g-', linewidth=2, label='Filtered accz')


# def decompose_frequencies(time, values, dt):
#     sp = fft(values)
#     freq = np.fft.fftfreq(time.shape[-1], d=dt)
#     return freq, sp

# def signal_creator(frequencies, components, t):
#     output = 0
#     for (frequency, component) in zip(frequencies, components):
#         output += component.real * np.cos(2 * np.pi * frequency * t)
#     return output

# frequencies, components = decompose_frequencies(t, accz, dt)

# time = np.linspace(0, 60, 1000)
# signal = [signal_creator(frequencies, components, t) for t in time]
# frequencies, components = decompose_frequencies(time, signal, time[-1]-time[-2])

# # components = components[frequencies < 0.55 and frequencies > 0.35]
# # frequencies = frequencies[frequencies < 0.55 and frequencies > 0.35]
# # plt.plot(frequencies, components.real)
# # y = butter_bandpass_filter(signal, lowcut, highcut, fs, order)
# # y = butter_lowpass_filter(signal, cutoff, fs, order)

# values = ifft(frequencies)

# plt.plot(time, values, label='recreated signal')

b, a = butter_bandpass(lowcut, highcut, fs, order=order)
padded_signal = filtfilt(b, a, accz)

plt.plot(t + 0.15, -padded_signal, label='padded signal')
plt.title("Data in '{}'".format(filename))
plt.legend(loc='upper right')
plt.xlabel('Time [sec]')
plt.show()

