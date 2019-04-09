# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:22:25 2019

@author: William
"""
import numpy as np
import settings
import pickle
import pygame
import os

save_path = os.path.join(os.getcwd(),"SPivotSwingEnv")
if not os.path.exists(save_path):
    os.makedirs(save_path)

oldest_gen = max([int(x.split(" ")[1].strip(".pkljg")) for x in os.listdir(save_path)])
oldest_str = "Generation "+str(oldest_gen)+".pkl"
gen_path = os.path.join(save_path, oldest_str)

nets = []
file = open(gen_path, "rb")
while True:
    try:
        nets.append(pickle.load(file))
    except EOFError:
        break
file.close()

nets = np.array(nets)
net_fits = np.array([net.fitness for net in nets])

net = nets[np.argmax(net_fits)]

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
link_sprites = pygame.sprite.Group()
layer_sprites = pygame.sprite.Group()

class Layer(pygame.sprite.Sprite):
    def __init__(self, layer):
        super().__init__()
        self.image = pygame.Surface([settings.pixel_per_layer, settings.screen_height], flags = pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0,0))
        self.number_nodes = len(layer)
        color = (0,0,0)
        if len(layer):
            self.pixel_per_row = settings.screen_height/len(layer)
        else:
            self.pixel_per_row = settings.screen_height
        for r in range(len(layer)):
            pos = (round(settings.pixel_per_layer/2), round(self.pixel_per_row*(r+.5)))
            pygame.draw.circle(self.image, (255,255,255), pos, settings.node_radius)
            pygame.draw.circle(self.image, color, pos, settings.node_radius, settings.node_width)

class Link(pygame.sprite.Sprite):
    def __init__(self, link, from_layer, from_node, double=False):
        super().__init__()
        self.image = pygame.Surface([settings.screen_width, settings.screen_height], flags = pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.from_ = (from_layer, from_node)
        self.to_ = link.connection
        if link.connection[0] == from_layer:
            #Draw a loop from the node to the same node
            color = (0,0,0)
            x = round((settings.pixel_per_layer*(from_layer+.5))+(3*settings.node_radius/2))
            y = round(layer_sprites.sprites()[from_layer].pixel_per_row*(from_node+.5))
            pygame.draw.circle(self.image, color, (x, y), settings.node_radius*2, 1)
        else:
            if double:
                color = (255, 0, 255)
            elif link.connection[0] < from_layer:
                color = (0,0,0)
            else:
                color = (0,0,255)
            x1 = round(settings.pixel_per_layer*(from_layer+.5))
            x2 = round(settings.pixel_per_layer*(link.connection[0]+.5))
            y1 = round(layer_sprites.sprites()[from_layer].pixel_per_row*(from_node+.5))
            y2 = round(layer_sprites.sprites()[link.connection[0]].pixel_per_row*(link.connection[1]+.5))
            pygame.draw.line(self.image, color, (x1,y1), (x2,y2), settings.link_width)

for l, layer in enumerate(net.nodes):
    layer_sprite = Layer(layer)
    layer_sprite.rect.x = settings.pixel_per_layer*l
    layer_sprite.rect.y = 0
    layer_sprites.add(layer_sprite)

for l,layer in enumerate(net.nodes):
    for n, node in enumerate(layer):
        for link in node.links:
            if link.weight:
                existing_links = link_sprites.sprites()
                double = False
                for existing_link in existing_links:
                    if (l, n) == existing_link.to_ and link.connection == existing_link.from_:
                        existing_link.kill()
                        double = True
                link_sprite = Link(link, l, n, double)
                link_sprite.rect.x = 0
                link_sprite.rect.y = 0
                link_sprites.add(link_sprite)

screen.fill((255, 255, 255))

#draw all sprites
link_sprites.draw(screen)
layer_sprites.draw(screen)

#update the screen
pygame.display.flip()
pygame.image.save(screen, os.path.join(save_path, "Best_Net_Gen {}.jpg".format(oldest_gen)))

done = False
try:
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
    pygame.quit()
except KeyboardInterrupt:
    pygame.quit()
