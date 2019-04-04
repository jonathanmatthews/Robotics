import numpy as np
import matplotlib.pyplot as plt

def format_graph(axis):
    """
    Works out if axis is a list of axis' or not, and if so individually formats each one
    """
    if isinstance(axis, np.ndarray):
        return [format_axis(ax) for ax in axis.flat]
    else:
        return format_axis(axis)

def format_axis(ax):
    """
    This formats an axis according to the style guidelines set below
    """
    plt.sca(ax)
    ax.set_facecolor('#eeeeee')
    plt.rcParams.update({'axes.titlesize': 18,
                         'legend.fontsize': 14,
                         'font.serif': 'Computer Modern Roman', })
    ax.yaxis.label.set_size(16)
    ax.xaxis.label.set_size(16)
    ax.minorticks_on()
    ax.xaxis.grid(b = True, which = 'both')
    ax.yaxis.grid(b = True, which = 'both')

    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    return ax

t_array_rotational_hinged = np.genfromtxt('TimeArray_Rotational_Hinged.csv', delimiter = ',')
swing_angles_rotational_hinged = np.genfromtxt('SwingAngles_Rotational_Hinged.csv', delimiter = ',')
peak_angles_rotational_hinged = np.genfromtxt('MaxAngles_Rotational_Hinged.csv', delimiter = ',')
body_positions_rotational_hinged = np.genfromtxt('BodyPositions_Rotational_Hinged.csv', delimiter = ',')
leg_positions_rotational_hinged = np.genfromtxt('LegPositions_Rotational_Hinged.csv', delimiter = ',')

t_array_rotational_no_hinge = np.genfromtxt('TimeArray_Rotational_NoHinge.csv', delimiter = ',')
swing_angles_rotational_no_hinge = np.genfromtxt('SwingAngles_Rotational_NoHinge.csv', delimiter = ',')
peak_angles_rotational_no_hinge = np.genfromtxt('MaxAngles_Rotational_NoHinge.csv', delimiter = ',')
body_positions_rotational_no_hinge = np.genfromtxt('BodyPositions_Rotational_NoHinge.csv', delimiter = ',')
leg_positions_rotational_no_hinge = np.genfromtxt('LegPositions_Rotational_NoHinge.csv', delimiter = ',')

t_array_parametric_hinged = np.genfromtxt('TimeArray_Parametric_Hinged.csv', delimiter = ',')
swing_angles_parametric_hinged = np.genfromtxt('SwingAngles_Parametric_Hinged.csv', delimiter = ',')
peak_angles_parametric_hinged = np.genfromtxt('MaxAngles_Parametric_Hinged.csv', delimiter = ',')
body_positions_parametric_hinged = np.genfromtxt('BodyPositions_Parametric_Hinged.csv', delimiter = ',')
leg_positions_parametric_hinged = np.genfromtxt('LegPositions_Parametric_Hinged.csv', delimiter = ',')

t_array_parametric_no_hinge = np.genfromtxt('TimeArray_Parametric_NoHinge.csv', delimiter = ',')
swing_angles_parametric_no_hinge = np.genfromtxt('SwingAngles_Parametric_NoHinge.csv', delimiter = ',')
peak_angles_parametric_no_hinge = np.genfromtxt('MaxAngles_Parametric_NoHinge.csv', delimiter = ',')
body_positions_parametric_no_hinge = np.genfromtxt('BodyPositions_Parametric_NoHinge.csv', delimiter = ',')
leg_positions_parametric_no_hinge = np.genfromtxt('LegPositions_Parametric_NoHinge.csv', delimiter = ',')

t_array_rotational_hinged_no_damping = np.genfromtxt('TimeArray_Rotational_Hinged_No_Damping.csv', delimiter = ',')
swing_angles_rotational_hinged_no_damping = np.genfromtxt('SwingAngles_Rotational_Hinged_No_Damping.csv', delimiter = ',')
peak_angles_rotational_hinged_no_damping = np.genfromtxt('MaxAngles_Rotational_Hinged_No_Damping.csv', delimiter = ',')

t_array_rotational_no_hinge_no_damping = np.genfromtxt('TimeArray_Rotational_NoHinge_No_Damping.csv', delimiter = ',')
swing_angles_rotational_no_hinge_no_damping = np.genfromtxt('SwingAngles_Rotational_NoHinge_No_Damping.csv', delimiter = ',')
peak_angles_rotational_no_hinge_no_damping = np.genfromtxt('MaxAngles_Rotational_NoHinge_No_Damping.csv', delimiter = ',')

t_array_parametric_hinged_no_damping = np.genfromtxt('TimeArray_Parametric_Hinged_No_Damping.csv', delimiter = ',')
swing_angles_parametric_hinged_no_damping = np.genfromtxt('SwingAngles_Parametric_Hinged_No_Damping.csv', delimiter = ',')
peak_angles_parametric_hinged_no_damping = np.genfromtxt('MaxAngles_Parametric_Hinged_No_Damping.csv', delimiter = ',')

t_array_parametric_no_hinge_no_damping = np.genfromtxt('TimeArray_Parametric_NoHinge_No_Damping.csv', delimiter = ',')
swing_angles_parametric_no_hinge_no_damping = np.genfromtxt('SwingAngles_Parametric_NoHinge_No_Damping.csv', delimiter = ',')
peak_angles_parametric_no_hinge_no_damping = np.genfromtxt('MaxAngles_Parametric_NoHinge_No_Damping.csv', delimiter = ',')

tmove_array_rotational_nohinge = np.genfromtxt('tmove_array_rotational_nohinge.csv', delimiter = ',')
max_angles_rotational_nohinge = np.genfromtxt('maximum_angles_rotational_nohinge.csv', delimiter = ',')

tmove_array_rotational_hinged = np.genfromtxt('tmove_array_rotational_hinged.csv', delimiter = ',')
max_angles_rotational_hinged = np.genfromtxt('maximum_angles_rotational_hinged.csv', delimiter = ',')

tmove_array_parametric_nohinge = np.genfromtxt('tmove_array_parametric_nohinge.csv', delimiter = ',')
max_angles_parametric_nohinge = np.genfromtxt('maximum_angles_parametric_nohinge.csv', delimiter = ',')
max_angles_parametric_nohinge[10] = 84.612366
max_angles_parametric_nohinge[11] = 84.55342

tmove_array_parametric_hinged = np.genfromtxt('tmove_array_parametric_hinged.csv', delimiter = ',')
max_angles_parametric_hinged = np.genfromtxt('maximum_angles_parametric_hinged.csv', delimiter = ',')


"""
# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        8, 6))




fig_1 = plt.figure(1)
plt.sca(ax)
plt.ylim([min(swing_angles_hinged), max(swing_angles_hinged)])
plt.ylabel("Swing Angle (rad)")
plt.xlabel("Time (s)")
plt.plot(t_array_hinged, swing_angles_hinged, color = 'r')
plt.savefig('Rotational_Hinged.pdf')

fig_2 = plt.figure(2)
plt.sca(ax)
plt.ylim([min(swing_angles_no_hinge), max(swing_angles_no_hinge)])
plt.ylabel("Swing Angle (rad)")
plt.xlabel("Time (s)")
plt.plot(t_array_no_hinge, swing_angles_no_hinge, color = 'r')
plt.savefig('Rotational_NoHinge.pdf')

fig_3 = plt.figure(3)
plt.plot(t_array_parametric_no_hinge, swing_angles_parametric_no_hinge)
plt.sca(ax)
plt.ylim([min(swing_angles_parametric_no_hinge), max(swing_angles_parametric_no_hinge)])
plt.ylabel("Swing Angle (rad)")
plt.xlabel("Time (s)")
plt.plot(t_array_parametric_no_hinge, swing_angles_parametric_no_hinge, color = 'r')
plt.savefig('Parametric_NoHinge.pdf')

fig_4 = plt.figure(4)
plt.plot(t_array_parametric_hinged, swing_angles_parametric_hinged)
plt.sca(ax)
plt.ylim([min(swing_angles_parametric_hinged), max(swing_angles_parametric_hinged)])
plt.ylabel("Swing Angle (rad)")
plt.xlabel("Time (s)")
plt.plot(t_array_parametric_hinged, swing_angles_parametric_hinged, color = 'r')
plt.savefig('Parametric_Hinged.pdf')

max_angle_hinged = np.max(abs(swing_angles_hinged))*180/np.pi
max_angle_no_hinge = np.max(abs(swing_angles_no_hinge))*180/np.pi
max_angle_parametric_no_hinge = np.max(abs(swing_angles_parametric_no_hinge))*180/np.pi
max_angle_parametric_hinged = np.max(abs(swing_angles_parametric_hinged))*180/np.pi
max_time_rotational_hinged = t_array_no_hinge[list(abs(swing_angles_hinged)).index(np.max(abs(swing_angles_hinged)))]
max_time_rotational_no_hinge = t_array_hinged[list(abs(swing_angles_no_hinge)).index(np.max(abs(swing_angles_no_hinge)))]
max_time_parametric_hinged = t_array_parametric_hinged[list(abs(swing_angles_parametric_hinged)).index(np.max(abs(swing_angles_parametric_hinged)))]
max_time_parametric_no_hinge = t_array_parametric_no_hinge[list(abs(swing_angles_parametric_no_hinge)).index(np.max(abs(swing_angles_parametric_no_hinge)))]

fig_1 = plt.figure(1)
plt.sca(ax)
plt.ylim([0, max(max_angles_parametric_nohinge)+5])
plt.ylabel("Max Angle Reached in 1000s - Rotational (rad)")
plt.xlabel("Tmove (s)")
plt.plot(tmove_array_rotational_nohinge, max_angles_rotational_nohinge, color = 'r')
plt.plot(tmove_array_rotational_hinged, max_angles_rotational_hinged, color = 'b')


plt.sca(ax)
plt.xlabel("Tmove (s)")
plt.plot(tmove_array_parametric_nohinge, max_angles_parametric_nohinge, color = 'c')
plt.plot(tmove_array_parametric_hinged, max_angles_parametric_hinged, color = 'g')
plt.legend(['Rotational No Hinge', 'Rotational Hinged', 'Parametric No Hinge', 'Parametric Hinged'])
plt.savefig('Different Tmoves No Damping.pdf')
"""
fig_1 = plt.figure(figsize = (8,6))
# use this to format graphs, keeps everything looking the same
ax = fig_1.add_subplot(1,1,1)
ax.set_facecolor('#eeeeee')
plt.ylim([0, max(max_angles_parametric_nohinge)+5])
plt.xlim([0.1, max(tmove_array_parametric_nohinge)])
plt.ylabel("Max Swing Angle (degrees)", fontsize = 16)
plt.xlabel("Tmove (s)", fontsize = 16)
plt.scatter(tmove_array_rotational_nohinge, max_angles_rotational_nohinge, color = 'r')
plt.scatter(tmove_array_rotational_hinged, max_angles_rotational_hinged, color = 'b')
plt.scatter(tmove_array_parametric_nohinge, max_angles_parametric_nohinge, color = 'c')
plt.scatter(tmove_array_parametric_hinged, max_angles_parametric_hinged, color = 'g')

fit_rotational_nohinge = np.poly1d(np.polyfit(tmove_array_rotational_nohinge,max_angles_rotational_nohinge, 1)) 
fit_rotational_hinged = np.poly1d(np.polyfit(tmove_array_rotational_hinged,max_angles_rotational_hinged, 1))
fit_parametric_nohinge = np.poly1d(np.polyfit(tmove_array_parametric_nohinge,max_angles_parametric_nohinge, 1))
fit_parametric_hinged = np.poly1d(np.polyfit(tmove_array_parametric_hinged,max_angles_parametric_hinged, 1))

plt.plot(tmove_array_rotational_nohinge, fit_rotational_nohinge(tmove_array_rotational_nohinge), color = 'r')
plt.plot(tmove_array_rotational_hinged, fit_rotational_hinged(tmove_array_rotational_hinged), color = 'b')
plt.plot(tmove_array_parametric_nohinge, fit_parametric_nohinge(tmove_array_parametric_nohinge), color = 'c')
plt.plot(tmove_array_parametric_hinged, fit_parametric_hinged(tmove_array_parametric_hinged), color = 'g')
plt.legend(['Rotational No Hinge', 'Rotational Hinged', 'Parametric No Hinge', 'Parametric Hinged'], fontsize = 11, loc = 1)
#plt.majorticks_on()
plt.minorticks_on()
plt.title('Maximum Swing Angle Reached in 1000s for Varying Tmove', fontsize = 18)

for xmaj in ax.xaxis.get_majorticklocs():
    ax.axvline(x=xmaj, ls='-', color = 'k', alpha = 0.4)
for xmin in ax.xaxis.get_minorticklocs():
    ax.axvline(x=xmin, ls='--', color = 'k', alpha = 0.2)

for ymaj in ax.yaxis.get_majorticklocs():
    ax.axhline(y=ymaj, ls='-', color = 'k', alpha = 0.4)
for ymin in ax.yaxis.get_minorticklocs():
    ax.axhline(y=ymin, ls='--', color = 'k', alpha = 0.2)

plt.savefig('Varying Tmove with Damping.pdf')

#plt.grid(b = True, which = 'major', axis = 'both', )

print(fit_rotational_nohinge)
print(fit_rotational_hinged)
print(fit_parametric_nohinge)
print(fit_parametric_hinged)


#plt.grid(b = True, which = 'major', axis = 'both')
"""
print('Max angle rotational no hinge damped = ' + str(max(peak_angles_rotational_no_hinge)))
print('Max angle rotational hinged damped = ' + str(max(peak_angles_rotational_hinged)))
print('Max angle parametric no hinge damped = ' + str(max(peak_angles_parametric_no_hinge)))
print('Max angle parametric hinged damped = ' + str(max(peak_angles_parametric_hinged)))

print('Max angle rotational no hinge no damping = ' + str(max(peak_angles_rotational_no_hinge_no_damping)))
print('Max angle rotational hinged no damping = ' + str(max(peak_angles_rotational_hinged_no_damping)))
print('Max angle parametric no hinge no damping = ' + str(max(peak_angles_parametric_no_hinge_no_damping)))
print('Max angle parametric hinged no damping = ' + str(max(peak_angles_parametric_hinged_no_damping)))
"""