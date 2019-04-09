# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:09:08 2019

@author: William
"""
input_nodes = 3
output_nodes = 1
max_layers = 6
max_layers += 1 #1 more than the number of hidden layers
initial_nodes = 100
initial_nodes += 1
maximum_nodes = 500
initial_links = 700
initial_links += 1
maximum_links = maximum_nodes*(input_nodes+1+output_nodes)+input_nodes*output_nodes

proportionality = 10.

min_link_change = 1
max_link_change = 5 #actually the range
max_link_change += 1
min_node_change = 1
max_node_change = 3 #actually the range
max_node_change += 1

regular_layer_bias = 0.8
in_out_layer_bias = 1-regular_layer_bias
#input_layer_weights = in_out_layer_bias*input_nodes/(input_nodes+output_nodes)
#output_layer_weights = in_out_layer_bias*output_nodes/(input_nodes+output_nodes)

number_nets = 100
repeats = 10
max_steps = 200
save_rate = 5
certain_parents = int(0.25*number_nets)
random_parents = int((number_nets/2)-certain_parents)
