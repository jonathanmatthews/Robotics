import Flail_redo_fixed_pygame as Sim
import pygame
import pygame.event
from pygame.locals import *
import numpy as np
import sys

def body_function(t,position,t_mid,current_period,tmove):
    if t_mid > 0:
        if position > 0:
            if (t-t_mid) < (current_period/4 - tmove):
                w = 0
            else:
                w = (body_angle_max-body_angle_min)/tmove
        if position <= 0:
            if (t-t_mid) < (current_period/4 - tmove):
                w = 0
            else:
                w = -(body_angle_max-body_angle_min)/tmove
    else:
        w = 0
    return w

def leg_function(t,position,t_mid,current_period,tmove):
    if t_mid > 0:
        if position > 0:
            if (t-t_mid) < (current_period/4 - tmove):
                w = 0
            else:
                w = (leg_angle_max - leg_angle_min)/tmove
        if position <= 0:
            if (t-t_mid) < (current_period/4 - tmove):
                w = 0
            else:
                w = -(leg_angle_max - leg_angle_min)/tmove
    else:
        w = 0
    return w
            
nat_period = 2.45
current_period = nat_period
tmove = 0.3
t = 0
t_array = []
mid_swings = [0]
swing_angles = []
body_positions = []
leg_positions = []
params = Sim.initialise()
position = 1
body_angle_min = np.pi/2-1.08756
body_angle_max = np.pi/2-0.60129
leg_angle_min = -np.pi/2-1.4
leg_angle_max = -np.pi/2+0.09208
max_angle = 0
max_angles = []

while t < 1000:
    t += 0.02
    t_array.append(t)
    
    body_motor_rate = body_function(t,position,mid_swings[-1],current_period,tmove)
    leg_motor_rate = leg_function(t,position,mid_swings[-1],current_period,tmove)
    
    output,params = Sim.stepper(*params,body_motor_rate,leg_motor_rate, max_angle)
    
    if abs(output[0]) > abs(max_angle):
        max_angle = abs(output[0])
    
    if len(swing_angles) >= 1:
        if np.sign(output[0]) != np.sign(swing_angles[-1]):
            if (t - mid_swings[-1]) > 0.3:
                mid_swings.append(t)
                
    
    position = np.sign(output[0])
    
    if len(mid_swings) >= 2:
        current_period = 2*(mid_swings[-1]-mid_swings[-2])

    swing_angles.append(output[0])
    body_positions.append(output[4])
    leg_positions.append(output[5])
    max_angles.append(max_angle*180/np.pi)
    """
np.savetxt('TimeArray_Rotational_NoHinge_No_Damping.csv', t_array, delimiter = ',')
np.savetxt('SwingAngles_Rotational_NoHinge_No_Damping.csv', swing_angles, delimiter = ',')
np.savetxt('MaxAngles_Rotational_NoHinge_No_Damping.csv', max_angles, delimiter = ',')
np.savetxt('BodyPositions_Rotational_NoHinge_No_Damping.csv', body_positions, delimiter = ',')
np.savetxt('LegPositions_Rotational_NoHinge_No_Damping.csv', leg_positions, delimiter = ',')

    """
    for event in pygame.event.get():
        if event.type == QUIT:
            #np.savetxt('TimeArray_Rotational_NoHinge.csv', t_array, delimiter = ',')
            #np.savetxt('SwingAngles_Rotational_NoHinge.csv', swing_angles, delimiter = ',')
            #np.savetxt('BodyPositions_Rotational_NoHinge.csv', body_positions, delimiter = ',')
            #np.savetxt('LegPositions_Rotational_NoHinge.csv', leg_positions, delimiter = ',')
            pygame.display.quit()
            pygame.quit()
            
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            #np.savetxt('TimeArray_Rotational_NoHinge.csv', t_array, delimiter = ',')
            #np.savetxt('SwingAngles_Rotational_NoHinge.csv', swing_angles, delimiter = ',')
            #np.savetxt('BodyPositions_Rotational_NoHinge.csv', body_positions, delimiter = ',')
            #np.savetxt('LegPositions_Rotational_NoHinge.csv', leg_positions, delimiter = ',')
            pygame.display.quit()
            pygame.quit()
#print(max_angle*180/np.pi)
#np.savetxt('TimeArray_Rotational_NoHinge_Damping2.csv', t_array, delimiter = ',')
#np.savetxt('SwingAngles_Rotational_NoHinge_Damping2.csv', swing_angles, delimiter = ',')