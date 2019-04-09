"""
Ben's Simulation with an animation
"""

import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *
import numpy as np
from pygame.color import *
from pymunk.vec2d import Vec2d

def add_swing(space):
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (300,300)

    swing = pymunk.Body()
    swing.position = (300,120)
    rod = pymunk.Segment(swing, (0, 180), (0, 0), 2.0)
    rod.mass = 2.5
    seat = pymunk.Poly(swing, [(-5, 3), (12, 3), (12,0),(-5,0)])
    seat.mass = 1.065

    ceiling_joint = pymunk.PivotJoint(swing, rotation_center_body, (0,179), (0,0))
    space.add(rod, seat, swing, ceiling_joint)

    return swing

def add_robot(space,seat):
    #define robot upper body and upper leg
    ubt = Vec2d(3.5,0)
    robot_u_points = [Vec2d(-4,31.64)+ubt,Vec2d(-4,0)+ubt,Vec2d(4,0)+ubt,Vec2d(4,31.64)+ubt]


    robot_body = pymunk.Body()
    robot_body.position = seat.position + (0,3)
    robot_u = pymunk.Poly(robot_body,robot_u_points)
    robot_u.mass = 3.311
    robot_u.color = THECOLORS["red"]
    robot_u.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)


    robot_u_leg = pymunk.Poly(seat,[(-0.5,3),(-10.5,3),(-10.5,8),(-0.5,8)])
    robot_u_leg.color = THECOLORS["red"]
    robot_u_leg.mass = 0.603

    #define robot lower leg
    robot_leg = pymunk.Body()
    robot_leg.position = seat.position
    robot_l_leg = pymunk.Poly(robot_leg,[(-10.5,5),(-10.5,-11.8),(-4.0,-11.8),(-4.0,5)])
    robot_l_leg.mass = 1.214
    robot_l_leg.color = THECOLORS["red"]
    space.add(robot_body,robot_u,robot_u_leg,robot_leg,robot_l_leg)

    #motor and pivot for hip
    #uses measured values of angles rather than given in program
    seat_motor = pymunk.SimpleMotor(seat,robot_body,0)
    seat_motor.max_force = 1e6
    seat_pivot = pymunk.PivotJoint(seat,robot_body,robot_body.position+ubt)
    seat_pivot._set_collide_bodies(False)
    seat_pivot_lim = pymunk.RotaryLimitJoint(robot_body,seat,0,0.575959)
    space.add(seat_motor,seat_pivot,seat_pivot_lim)

    #motor and pivot for knee
    max_knee_ang = 0.34
    knee_motor = pymunk.SimpleMotor(seat,robot_leg,0)
    knee_motor.max_force = 1e5
    knee_pivot = pymunk.PivotJoint(seat,robot_leg,seat.position+(-8,7))
    knee_pivot._set_collide_bodies(False)
    knee_pivot_lim = pymunk.RotaryLimitJoint(seat,robot_leg,max_knee_ang-np.deg2rad(69),max_knee_ang)
    space.add(knee_motor,knee_pivot,knee_pivot_lim)

    return seat_motor,knee_motor,robot_body,robot_leg

def initialise():
    damping_coeff = np.exp(-2.56*np.deg2rad(0.0034))

    space = pymunk.Space()
    space.gravity = (0, -981)
    space.damping = damping_coeff

    swing = add_swing(space)
    seat_motor,knee_motor,robot_u,leg = add_robot(space,swing)

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("I'm so swungover")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    return [space,swing,robot_u,seat_motor,knee_motor,leg,screen,draw_options,clock,font]

def stepper(space,swing,robot_u,seat_motor,knee_motor,leg,screen,draw_options,clock,font,action):
    if action == 1:
        seat_motor.rate = 1.91986
        knee_motor.rate = 4.01426
    elif action == 0:
        seat_motor.rate = -1.91986
        knee_motor.rate = -4.01426

    screen.fill((255,255,255))
    space.debug_draw(draw_options)
    screen.blit(font.render("Angle = " + str(np.rad2deg(swing.angle)),1, THECOLORS["black"]), (0,0))
    screen.blit(font.render("Swing Velocity = " + str(swing._get_angular_velocity()),1, THECOLORS["black"]), (0,20))
    pygame.display.flip()
    clock.tick(50)

    for _ in range(4):
        space.step(0.005)

    #return values
    angle = swing.angle
    ang_vel = swing._get_angular_velocity()
    body_pos = robot_u.angle

    tot_mass = swing.mass + robot_u.mass + leg.mass
    tot_kinetic_energ = leg._get_kinetic_energy() + swing._get_kinetic_energy()+ robot_u._get_kinetic_energy()
    tot_COM_y = ((swing.position[1]+swing._get_center_of_gravity()[1])*swing.mass + (leg.position[1]+leg._get_center_of_gravity()[1])*leg.mass + (robot_u.position[1]+robot_u._get_center_of_gravity()[1])*robot_u.mass)/tot_mass
    tot_grav_energ = tot_COM_y*tot_mass*np.abs(space.gravity[1] )
    energy = tot_kinetic_energ+tot_grav_energ

    return [angle, ang_vel, body_pos],[space,swing,robot_u,seat_motor,knee_motor,leg,screen,draw_options,clock,font], energy

