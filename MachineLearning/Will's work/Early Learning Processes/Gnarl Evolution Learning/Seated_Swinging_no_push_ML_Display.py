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

    swing = pymunk.Body()
    swing.position = (300,121)
    rod = pymunk.Segment(swing, (0, 179), (0, 0), 2.0)
    rod.mass = 2.5
    seat = pymunk.Poly(swing, [(-5, 2), (5, 2), (5,-2),(-5,-2)])
    seat.mass = 1.065

    ceiling_joint = pymunk.PinJoint(swing, rotation_center_body, (0,179), (0,0))
    space.add(rod, seat, swing, ceiling_joint)

    return swing

def add_robot(space,swing):
    #define robot upper body and upper leg
    robot_body = pymunk.Body()
    robot_u = pymunk.Poly(robot_body,[(-4,31.64),(-4,0),(4,0),(4,31.64)])
    robot_u.mass = 3.311
    robot_u.color = THECOLORS["red"]
    robot_body.position = swing.position
    robot_u_leg = pymunk.Poly(swing,[(0,2),(-15,2),(-15,8),(0,8)])
    robot_u_leg.color = THECOLORS["red"]
    robot_u_leg.mass = 0.603

    #define robot lower leg
    robot_leg = pymunk.Body()
    robot_leg.position = swing.position
    robot_l_leg = pymunk.Poly(robot_leg,[(-15,2),(-15,-14.8),(-9,-14.8),(-9,2)])
    robot_l_leg.mass = 1.214
    robot_l_leg.color = THECOLORS["red"]
    space.add(robot_body,robot_u,robot_u_leg,robot_leg,robot_l_leg)

    #motor and pivot for hip
    seat_motor = pymunk.SimpleMotor(swing,robot_body,0)
    seat_motor.max_force = 1e6
    seat_pivot = pymunk.PivotJoint(swing,robot_body,swing.position)
    seat_pivot._set_collide_bodies(False)
    seat_pivot_lim = pymunk.RotaryLimitJoint(robot_body,swing,0,np.pi/4)
    space.add(seat_motor,seat_pivot,seat_pivot_lim)

    #motor and pivot for knee
    knee_motor = pymunk.SimpleMotor(swing,robot_leg,0)
    knee_motor.max_force = 1e5
    knee_pivot = pymunk.PivotJoint(swing,robot_leg,swing.position+(-13,2))
    knee_pivot._set_collide_bodies(False)
    knee_pivot_lim = pymunk.RotaryLimitJoint(swing,robot_leg,-np.pi/4,np.pi/4)
    space.add(knee_motor,knee_pivot,knee_pivot_lim)

    return seat_motor,knee_motor,robot_body

def initialise():
    space = pymunk.Space()
    space.gravity = (0.0, -981)
    space.damping = 1.#0.9

    swing = add_swing(space)
    seat_motor,knee_motor,robot_u = add_robot(space,swing)
    #swing.apply_force_at_local_point((-40000, 0), (0,0))

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("I'm so swungover")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    return [space,swing,robot_u,seat_motor,knee_motor,screen,draw_options,clock,font]

def stepper(space,swing,robot_u,seat_motor,knee_motor,screen,draw_options,clock,font,action):
    if action == 2:
        seat_motor.rate = 3
        knee_motor.rate = 6
    elif action == 1:
        seat_motor.rate = 0
        knee_motor.rate = 0
    elif action == 0:
        seat_motor.rate = -3
        knee_motor.rate = -6

    screen.fill((255,255,255))
    space.debug_draw(draw_options)
    screen.blit(font.render("Angle = " + str(np.rad2deg(np.arctan((swing.position[0]-300)/(swing.position[1]-300)))),1, THECOLORS["black"]), (0,0))
    screen.blit(font.render("Swing Velocity = " + str(swing.velocity),1, THECOLORS["black"]), (0,20))
    pygame.display.flip()
    clock.tick(50)

    space.step(1.0/50.0)

    #return values
    angle = np.arctan((swing.position[0]-300)/(swing.position[1]-300))
    if swing.position[1] > 300:
        if swing.position[0] < 300:
            angle = np.pi + angle
        elif swing.position[0] > 300:
            angle = -np.pi + angle
    vel = [swing.velocity[0],swing.velocity[1]]
    body_pos = robot_u.angle

    return [angle, vel[0], vel[1], body_pos],[space,swing,robot_u,seat_motor,knee_motor,screen,draw_options,clock,font]

