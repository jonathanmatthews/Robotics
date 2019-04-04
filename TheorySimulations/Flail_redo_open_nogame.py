import sys, random
import pygame
import pymunk
import pymunk.pygame_util
from pygame.locals import *
import numpy as np
from pygame.color import *
import operator

max_angle = 0

def add_swing(space):
    swing_pivot = pymunk.Body(body_type = pymunk.Body.STATIC)
    swing_pivot.position = (300,300)
    
    urod_end = pymunk.Body()
    urod_length = (0,154)
    urod_end.position = swing_pivot.position + urod_length
    #urod_end.angle = -2*np.pi/180
    urod_end.angular_velocity = -0.6
    #urod_end.apply_force_at_local_point(urod_end.position,(-1000,0))
    
    lrod_end = pymunk.Body()
    lrod_length = (0,26)
    lrod_end.position = urod_end.position + lrod_length
    #lrod_end.angle = -2*np.pi/180
    lrod_end.angular_velocity = 0
    #lrod_end.apply_force_at_local_point(lrod_end.position,(-100,0))
    
    urod = pymunk.Segment(urod_end, (0,0), (0,154), 2)
    urod.mass = 2.2
    urod.filter = pymunk.ShapeFilter(categories=0b1, mask = 0b0)
    urod.color = THECOLORS["black"]
    
    lrod = pymunk.Segment(lrod_end, (0,0), (0,26), 2)
    lrod.mass = 0.3
    lrod.filter = pymunk.ShapeFilter(categories=0b1, mask = 0b0)
    lrod.color = THECOLORS["blue"]
    
    seat = pymunk.Circle(lrod_end,2)
    seat.mass = 2.352
    seat.filter = pymunk.ShapeFilter(categories=0b1, mask = 0b0)
    seat.color = THECOLORS["red"]
    
    swing_joint = pymunk.PivotJoint(swing_pivot, urod_end, (0,0), urod_length)
    swing_joint._set_collide_bodies(False)
    
    middle_joint = pymunk.PivotJoint(urod_end, lrod_end, (0,0), lrod_length)
    middle_joint._set_collide_bodies(False)
    
    #in order to make it a single rod
    #middle_joint_lim = pymunk.RotaryLimitJoint(urod_end,lrod_end,0,0)
    
    middle_fric = pymunk.GearJoint(urod_end,lrod_end,0,1)
    middle_fric.max_force = 5000
    
    space.add(urod, lrod, seat, swing_pivot, urod_end, lrod_end, swing_joint, middle_joint, middle_fric)#, middle_joint_lim)
    
    return urod_end, lrod_end

def add_robot(space, urod_end, lrod_end):
    #define limits of robot movement
    body_angle_min = np.pi/2-1.13756 #include estimated head movement
    body_angle_max = np.pi/2-0.55129 #include estimated head movement
    #body_angle_min = np.pi/2-1.08756
    #body_angle_max = np.pi/2-0.60129
    leg_angle_min = -np.pi/2-1.4
    leg_angle_max = -np.pi/2+0.09208
    
    robot_body = pymunk.Body()
    body_length = (0,31.6)
    robot_body.position = lrod_end.position
    robot_body.angular_velocity = 0
    body = pymunk.Segment(robot_body, body_length, (0,0),2)
    body.mass = 3.311
    body.filter = pymunk.ShapeFilter(categories=0b1,mask = 0b0)
    body.color = THECOLORS["pink"]
    
    robot_leg = pymunk.Body()
    leg_length = (0,25)
    robot_leg.position = lrod_end.position
    robot_leg.angular_velocity = 0
    leg = pymunk.Segment(robot_leg, leg_length, (0,0), 2)
    leg.mass = 1.214 + 0.8
    leg.filter = pymunk.ShapeFilter(categories=0b1,mask = 0b0)
    leg.color = THECOLORS["green"]

    body_motor = pymunk.SimpleMotor(lrod_end,robot_body,0)
    body_motor.max_force = 1e5
    
    body_pivot = pymunk.PivotJoint(lrod_end,robot_body,lrod_end.position)
    body_pivot._set_collide_bodies(False)
    
    body_pivot_lim = pymunk.RotaryLimitJoint(robot_body,lrod_end,body_angle_min,body_angle_max)
    
    #motor and pivot for leg
    leg_motor = pymunk.SimpleMotor(lrod_end,robot_leg,0)
    leg_motor.max_force = 1e5
    
    leg_pivot = pymunk.PivotJoint(lrod_end,robot_leg,lrod_end.position)
    leg_pivot._set_collide_bodies(False)
    
    leg_pivot_lim = pymunk.RotaryLimitJoint(robot_leg,lrod_end,leg_angle_min,leg_angle_max)
    
    space.add(robot_body, body, robot_leg, leg, body_motor, body_pivot, body_pivot_lim, leg_motor, leg_pivot, leg_pivot_lim)
    
    return robot_body, robot_leg, body_motor, leg_motor

def initialise():
    space = pymunk.Space()
    space.gravity = (0, -981)
    space.damping = np.exp(-2.56*0.0034)
    
    #pygame.init()
    #screen = pygame.display.set_mode((600, 600))
    #pygame.display.set_caption("Double_hinge_flail")
    #clock = pygame.time.Clock()
    #font = pygame.font.SysFont("Arial", 16)
    #draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 0b0)
    
    urod_end, lrod_end = add_swing(space)
    robot_body, robot_leg, body_motor, leg_motor = add_robot(space,urod_end,lrod_end)
    
    return [space, urod_end, lrod_end, robot_body, robot_leg, body_motor, leg_motor] #screen, draw_options, clock, font]

def stepper(space, urod_end, lrod_end, robot_body, robot_leg, body_motor, leg_motor, body_motor_rate, leg_motor_rate, max_angle): #screen, draw_options, clock, font,
    body_motor.rate = body_motor_rate
    leg_motor.rate = leg_motor_rate
    
    #screen.fill((255,255,255))
    #space.debug_draw(draw_options)
    #screen.blit(font.render("Angle = " + str(urod_end._get_angle()),1, THECOLORS["black"]), (0,0))
    #screen.blit(font.render("Swing Velocity = " + str(urod_end._get_angular_velocity()),1, THECOLORS["black"]), (0,20))
    #screen.blit(font.render("Max Angle = " + str(max_angle*180/np.pi),1, THECOLORS["black"]), (0,40))
    #pygame.display.flip()
    #clock.tick(50)
    
    space.step(1.0/50.0)
    
    #return values
    urod_angle = urod_end._get_angle()
    urod_ang_vel = urod_end._get_angular_velocity()
    lrod_angle = lrod_end._get_angle()
    lrod_ang_vel = lrod_end._get_angular_velocity()
    body_pos = robot_body._get_angle()-lrod_angle
    leg_pos = robot_leg._get_angle()-lrod_angle
    
    
    return [urod_angle, urod_ang_vel, lrod_angle, lrod_ang_vel, body_pos, leg_pos],\
           [space, urod_end, lrod_end, robot_body, robot_leg, body_motor, leg_motor] #screen, draw_options, clock, font]