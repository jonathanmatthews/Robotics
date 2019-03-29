from sys import path
path.append("..")

import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from utility_functions import read_file
from graph_functions import format_graph

#parametric = read_file("../Output_data/Parametric No Masses 800secs")['be']
#rotational = read_file("../Output_data/Rotational No Masses 400secs")['be']

parametric = read_file("../Output_data/26-03-2019 18:17:02 Para 600 secs Org")
rotational = read_file("../Output_data/26-03-2019 18:30:45 Rot 600 secs Org")

para_dt = np.mean(np.diff(parametric['time']))
rot_dt = np.mean(np.diff(rotational['time']))

index_para = find_peaks(parametric['be'])[0]
index_rot = find_peaks(rotational['be'])[0]

peaks_para = abs(parametric['be'][index_para])
peaks_rot = abs(rotational['be'][index_rot])

times_para = parametric['time'][index_para]
times_rot = abs(rotational['time'][index_rot])



##### George's magical filter.
be = peaks_para
t = times_para
no_large_change_indexes = np.diff(be) < 0.25
t = t[:-1][no_large_change_indexes]
be = be[:-1][no_large_change_indexes]
peaks_para = be
times_para = t
#####

n_para = times_para
n_rot = times_rot

t_para = np.arange(len(peaks_para))*para_dt/2.55
t_rot = np.arange(len(peaks_rot))*rot_dt/2.55

def fit_rotational(n, m, c):
    """
    Function to fit for rotational curve. Linear function.
    n : cycle number,
    m : gradient,
    c : y-intercept.
    """
    # Linear.
    return m*n + c

def fit_parametric(n, m, c, q, k):
    """
    Function to fit for parametric curve. Piecewise function of linear then exponential.
    n : cycle number,
    m : linear gradient,
    c : y-intercept of linear,
    q : cycle number at which to change to exponential,
    k : exponent factor.

    Don't bother with this one, this is just here incase I need it in the future.
    """
    # Linear then exponential.
    # y(n<q) = mn+c
    # y(n>=q) = (mq+c) e^k(n-q)
    lin = lambda n: m * n + c
    exp = lambda n: (m * q + c) * np.exp(k * (n - q))
    ans = np.piecewise(n, [n < q, n >= q], [lin, exp])
    #print ans
    return ans

def fit_parametric_2(n, k, a, c):
    return a*np.exp(k*n) + c

def plot_rot():
    """
    Fit linear region of rotational, then plot.
    This function only exists for testing values on rotational.
    """
    rot_params = curve_fit(fit_rotational, n_rot[20:61], peaks_rot[20:61])
    # Linear region seems to end at ~100 cycles.
    fitted_rot = fit_rotational(n_rot[:101], *rot_params[0])
    eqn_rot = "{} n + {}".format(round(rot_params[0][0], 3), round(rot_params[0][1], 3))

    fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
    ax.set_facecolor("#eeeeee")

    plt.plot(n_rot[:101], fitted_rot, Label="Rotational (Quarter Period)")
    plt.plot(n_rot, peaks_rot, 'g.', label=r"Linear fit, $\theta$ = " + eqn_rot)
    plt.xlabel("Cycle number")
    plt.ylabel(r"Amplitude ($^o$)")
    plt.title("Fit of rotational amplitude gain")
    #plt.set_facecolor('#eeeeee')
    plt.legend()
    plt.show()

def plot_para():
    """
    Fit linear/exponential region of parametric, then plot.
    This function exists only for testing values on parametric.
    """
    #print [len(n_para), len(peaks_para)]

    para_params = curve_fit(fit_parametric_2, n_para[35:250], peaks_para[35:250], p0=[0.0064, 1, 0])
    print para_params[0]
    fitted_para = fit_parametric_2(n_para[35:250], *para_params[0])
    eqn_para = "{} exp({} n) + {}".format(round(para_params[0][1], 3), round(para_params[0][0], 3), round(para_params[0][2], 3))
    #eqn_para = ""

    fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
    ax.set_facecolor("#eeeeee")

    plt.plot(n_para, peaks_para, "g.", Label="Parametric (Quarter Period)")
    plt.plot(n_para[35:250], fitted_para, label=r"exponential fit, $\theta$ = " + eqn_para)
    plt.xlabel("Cycle number")
    plt.ylabel(r"Amplitude ($^o$)")
    plt.title("Fit of parametric amplitude gain")
    plt.legend()
    plt.show()

def plot_both():
    # Get rotational.
    rot_params = curve_fit(fit_rotational, n_rot[20:61], peaks_rot[20:61])
    # Linear region seems to end at ~100 cycles.
    fitted_rot = fit_rotational(n_rot[20:61], *rot_params[0])
    eqn_rot = "{} n + {}".format(round(rot_params[0][0], 3), round(rot_params[0][1], 3))

    fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))
    ax.set_facecolor("#eeeeee")

    plt.plot(n_rot, peaks_rot, '.', color="#00004d", Label="Rotational (Quarter Period)")
    plt.plot(n_rot[20:61], fitted_rot, color="#456DBA", label=r"Linear fit, $\theta$ = " + eqn_rot)
    plt.xlabel("Cycle number")
    plt.ylabel(r"Amplitude ($^o$)")
    #plt.set_facecolor('#eeeeee')

    ax = format_graph(ax)

    # Get parametric.
    para_params = curve_fit(fit_parametric_2, n_para[20:90], peaks_para[20:90], p0=[np.log(4)/26, 1, 0])
    print para_params[0]
    fitted_para = fit_parametric_2(n_para[20:90], *para_params[0])
    eqn_para = "{} exp({} n) + {}".format(round(para_params[0][1], 3), round(para_params[0][0], 5), round(para_params[0][2], 3))
    #eqn_para = ""
    print "parametric errors: {}".format(np.sqrt(np.diag(para_params[1])))
    print "rotational errors: {}".format(np.sqrt(np.diag(rot_params[1])))

    plt.plot(n_para, peaks_para, ".", color="#CC0000", Label="Parametric (Quarter Period)")
    plt.plot(n_para[20:90], fitted_para, color="#F9A628", label=r"exponential fit, $\theta$ = " + eqn_para)
    plt.xlabel("Period number")
    plt.ylabel(r"Amplitude ($^o$)")
    plt.title("Fit of per-period amplitude gain")
    plt.legend()
    plt.show()


#plot_rot()
#plot_para()
plot_both()


#plt.plot(t_para, peaks_para)
#plt.show()



