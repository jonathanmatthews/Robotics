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
    seat = pymunk.Poly(swing, [(-20.0, 4), (20.0, 4), (20,-4),(-20,-4)])
    seat.mass = 1.065

    ceiling_joint = pymunk.PinJoint(swing, rotation_center_body, (0,179), (0,0))
    space.add(rod, seat, swing, ceiling_joint)

    return swing


def add_robot(space,swing):
    robot = []
    num_circles = 20
    circle_height = [15,95]
    circle_rad = (circle_height[1]-circle_height[0])/(2*(num_circles-1))


    for i in range(num_circles):
        robot.append(pymunk.Circle(swing, circle_rad, (0,circle_height[0]+(2*i*circle_rad))))
        robot[i].mass = 0
        space.add(robot[i])

    return robot

def initialise():
    space = pymunk.Space()
    space.gravity = (0.0, -981)
    space.damping = 0.9

    swing = add_swing(space)
    robot = add_robot(space,swing)
    swing.apply_force_at_local_point((-40000,0),(0,0))

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("I'm so swungover")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    return [space,swing,robot,0,screen,draw_options,clock,font]

def stepper(space,swing,robot,target_pos,screen,draw_options,clock,font,action):
    num_circles = 20
    robot_mass = 5
    swing_mom = [13798,18421]
    mom_step = (swing_mom[1]-swing_mom[0])/(num_circles-1)

    if action == 2:
        if target_pos < (num_circles-1):
            target_pos += 1
    if action == 0:
        if target_pos > 0:
            target_pos -= 1

    for i in range(len(robot)):
        if i == target_pos:
            robot[i].color = THECOLORS["red"]
            robot[i].mass = robot_mass
        else:
            robot[i].color = THECOLORS["blue"]
            robot[i].mass = 0

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
    vel = swing.velocity
    body_pos = target_pos

    return [angle, vel[0], vel[1], body_pos],[space,swing,robot,target_pos,screen,draw_options,clock,font]

