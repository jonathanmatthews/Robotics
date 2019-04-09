import sys, random
import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *
import numpy as np
from pygame.color import *

def add_swing(space):
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300,300)

    rod = pymunk.Body()
    rod.position = (300,138)
    rod_u = pymunk.Segment(rod, (0,162), (0,0), 2.0)
    rod_u.mass = 2.2
    rod_u.filter = pymunk.ShapeFilter(categories=1)
    rod_u.color = THECOLORS["black"]

    seat_pivot = pymunk.Body()
    seat_pivot.position = (300,118)
    rod_l = pymunk.Segment(seat_pivot, (0,20), (0,0), 2.0)
    rod_l.mass = 0.3
    rod_l.color = THECOLORS["green"]


    seat = pymunk.Poly(seat_pivot, [(-5, 2), (5, 2), (5,-2),(-5,-2)])
    seat.mass = 1.065
    seat.color = THECOLORS["pink"]

    ceiling_joint = pymunk.PivotJoint(rod, rotation_center_body, (0,162), (0,0))
    pivot_joint = pymunk.PivotJoint(rod,seat_pivot,(0,0),(0,20))
    pivot_joint._set_collide_bodies(False)
    pivot_fric = pymunk.GearJoint(rod,seat_pivot,0,1)
    pivot_fric.max_force = 1000
    space.add(rod_u,rod_l, seat, rod, seat_pivot, ceiling_joint, pivot_joint,pivot_fric)

    return rod,seat_pivot

def add_robot(space,rod,seat):
    #define robot upper body and upper leg
    robot_body = pymunk.Body()
    robot_u = pymunk.Poly(robot_body,[(-4,31.64),(-4,0),(4,0),(4,31.64)])
    robot_u.mass = 3.311
    robot_u.color = THECOLORS["red"]
    robot_u.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)

    robot_body.position = seat.position
    robot_u_leg = pymunk.Poly(seat,[(0,2),(-15,2),(-15,8),(0,8)])
    robot_u_leg.color = THECOLORS["red"]
    robot_u_leg.mass = 0.603

    #define robot lower leg
    robot_leg = pymunk.Body()
    robot_leg.position = seat.position
    robot_l_leg = pymunk.Poly(robot_leg,[(-15,2),(-15,-14.8),(-9,-14.8),(-9,2)])
    robot_l_leg.mass = 1.214
    robot_l_leg.color = THECOLORS["red"]
    space.add(robot_body,robot_u,robot_u_leg,robot_leg,robot_l_leg)

    #motor and pivot for hip
    seat_motor = pymunk.SimpleMotor(seat,robot_body,0)
    seat_motor.max_force = 1e6
    seat_pivot = pymunk.PivotJoint(seat,robot_body,seat.position)
    seat_pivot._set_collide_bodies(False)
    seat_pivot_lim = pymunk.RotaryLimitJoint(robot_body,seat,0,1.11529)
    space.add(seat_motor,seat_pivot,seat_pivot_lim)

    #motor and pivot for knee
    knee_motor = pymunk.SimpleMotor(seat,robot_leg,0)
    knee_motor.max_force = 1e5
    knee_pivot = pymunk.PivotJoint(seat,robot_leg,seat.position+(-13,2))
    knee_pivot._set_collide_bodies(False)
    knee_pivot_lim = pymunk.RotaryLimitJoint(seat,robot_leg,-1.04604,0.44604)
    space.add(knee_motor,knee_pivot,knee_pivot_lim)

    return seat_motor,knee_motor,robot_body


def initialise():
    space = pymunk.Space()
    space.gravity = (0, -981)
    space.damping = 0.95

    swing,seat = add_swing(space)
    seat_motor,knee_motor,robot_u = add_robot(space,swing,seat)

    swing.apply_force_at_local_point((40000,0),(0,0))

    return [space,swing,seat,robot_u,seat_motor,knee_motor]

def stepper(space,swing,seat,robot_u,seat_motor,knee_motor,action):
    if action == 2:
        seat_motor.rate = 2.788225
        knee_motor.rate = 3.7302
    elif action == 1:
        seat_motor.rate = 0
        knee_motor.rate = 0
    elif action == 0:
        seat_motor.rate = -2.788225
        knee_motor.rate = -3.7302

    space.step(1.0/50.0)

    #return values
    rod_angle = swing._get_angle()
    rod_ang_vel = swing._get_angular_velocity()
    seat_angle = seat._get_angle()
    seat_ang_vel = seat._get_angular_velocity()
    body_pos = robot_u._get_angle()-seat_angle

    return [rod_angle,rod_ang_vel,seat_angle,seat_ang_vel,body_pos],[space,swing,seat,robot_u,seat_motor,knee_motor]

