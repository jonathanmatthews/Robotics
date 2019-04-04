import numpy as np
import os
import matplotlib.pyplot as plt
from graph_functions import *
from sys import path, argv
path.insert(0, '..')
from utility_functions import read_file, get_latest_file, total_angle


test = False
if argv[-1] == 'Testing':
    test = True
if argv[-1] == 'Real':
    test = False

# access latest file if underneath file name is blanked out
<<<<<<< HEAD
filename, output_data_directory = get_latest_file('Analysis', test=test)
=======
# filename, output_data_directory = get_latest_file('Analysis', test=test)
output_data_directory = '../Output_data/'
filename = '22-03-2019 14:00:36 Org'
>>>>>>> master
angles = read_file(output_data_directory + filename)

# Extract data
t = angles['time']
be = angles['be']
position = angles['pos']
algorithm = angles['algo']
<<<<<<< HEAD
=======
se0 = angles['se0']
se1 = angles['se1']
te = total_angle(be, se0, se1)

# adjusted_angle = total_angle(be-be[0], se0, se1) 
>>>>>>> master

# setup figure
fig, ax = plt.subplots(
    1, 1, figsize=(
        13, 8))

#ax = format_graph(ax)


# editing plot that will show angle
plt.sca(ax)
shade_background_based_on_algorithm(t, algorithm)

# adding titles etc, this will add to ax
<<<<<<< HEAD
plt.title('Determining when to kick using angular velocity')
=======
# plt.title('Determining when to kick using the max angle')
# plt.title('Determining when to kick using the quarter period')
plt.title('Old Joe')
# plt.title('Plot of angle, named position, and algorithm being run. \n Data taken from {}'.format(filename))
# plt.title('Parametric pumping using quarter period algorithm')
# plt.title('Rotational pumping using quarter period algorithm')
>>>>>>> master
plt.xlabel('Time (s)')
plt.ylabel('Angle ' + r"$(^o)$")

# t = t[be < 30]
# be = be[be < 30]

# plotting angle versus time
plt.plot(t, be-be[0], label='Big Encoder', color='b')
# plt.plot(t, te, label='Total Angle', color='b')
plt.xlim([0, max(t)])

# editing axis that will have named positions on
<<<<<<< HEAD
if test:
=======
#if test:
if False:
>>>>>>> master
    # make a copy of axis and overlay it, this way can have angles and named position on same plot
    ax2 = ax.twinx()
    ax2 = format_graph(ax2)
    plt.sca(ax2)
    add_named_position_plot(t, position)
    # make one big legend not two smaller ones
    combine_multiple_legends([ax, ax2], custom_location='lower left')
else:
<<<<<<< HEAD
    plt.legend(loc='upper left')

plt.show()
# fig.savefig(
    # 'Figures/{}.png'.format(filename), format='png')
=======
    plt.legend(loc='lower right')
# plt.xlim([30, 40])
# # plt.xlim([16, 24])
# # plt.axvspan(16, 24, alpha = 0.1, color='grey')

# # # Only want this to illustrate how Nao figures out when to change for seminar
# ax3 = zoomed_inset_axes(ax, 16, loc=1)
# plt.sca(ax3)

# x1, x2, y1, y2 = 32.9, 33.25, 2.1, 2.9
# # x1, x2, y1, y2 = 43.0, 43.2, 3.0, 4.0
# # x1, x2, y1, y2 = 43.1, 43.6, 2.3, 3.7
# ax3.set_xlim(x1, x2)
# ax3.set_ylim(y1, y2)
# ax3.set_facecolor('#eeeeee')
# plt.xticks(visible=False)
# plt.yticks(visible=False)
# plt.plot(t, be-be[0])
# plt.ylabel('')
# plt.xticks([])
# plt.yticks([])
# # position_number = [position_numbers[i]*0.4 + 3.5 for i in position]
# # position_number = [position_numbers[i]*0.4 + 3.0 for i in position]
# position_number = [position_numbers[i]*0.25 + 2.5 for i in position]


# plt.plot(t, position_number, color='r', linewidth=0.5)
# # plt.axvspan(16, 24, alpha = 0.1, color='grey')

# # plt.plot(t + 0.25, position_number, color='g', linewidth=0.5)

# mark_inset(ax, ax3, loc1=2, loc2=3, ec="0.5", fc="w")

fig.tight_layout()
plt.show()
# fig.savefig(
    # 'Figures/{}.eps'.format(filename), format='eps')
# fig.savefig(
    # 'Figures/DoublePendulumRotationalAngular.pdf', format='pdf'
# )

fig.savefig(
    'Figures/OldJoe.pdf', format='pdf'
)
>>>>>>> master
