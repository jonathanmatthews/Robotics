# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:30:16 2019

Provides the classes for the Nets to opperate

@author: William
"""
from sigmoid import sigmoid
import settings
import numpy as np
import random

class Link:
    """
    The small link class for transfering data between nodes
    """
    def __init__(self, net, connection, weight=0):
        self.net = net
        self.connection = connection #tuple of (layer, specific)
        self.weight = weight

    def output(self):
        """
        Checks it's input node and recalculates it's output
        """
        return self.weight*self.net.nodes[self.connection[0]][self.connection[1]].output

    def mutate(self, std_dev):
        """
        Alters it's weight based on the tempertaure from the StdDev provided
        """
        self.weight += np.random.normal(0, std_dev)

class Node:
    """
    The nodes which perform the majority of maths for the net
    """
    def __init__(self, net, bias=0):
        self.net = net
        self.bias = bias
        self.links = np.array([], dtype=object)
        self.output = None
        self._output()

    def _output(self):
        """
        Updates all its links then recalculates it's output
        """
        total = sum(link.output() for link in self.links)
        total += self.bias
        self.output = sigmoid(total)

    def add_link(self, connection, weight=0):
        """
        Appends a new link to it's link array
        """
        self.links = np.append(self.links, Link(self.net, connection, weight))

    def mutate(self, std_dev):
        """
        Triggers mutation in all of its links then mutates its own bias
        based on the temperature from the StdDev provided
        """
        for link in self.links:
            link.mutate(std_dev)
        self.bias += np.random.normal(0, std_dev)

    def __repr__(self):
        """
        A really ugly, barely useful representation of the node
        """
        strng = "Node(bias={},links=".format(self.bias)
        for link in self.links:
            strng += "(weight={},connection={})".format(link.weight, link.connection)
        strng += ")"
        return strng

    def clear(self):
        """
        Recalculates the output with no links.
        Removes 'memories' from back links
        """
        self.output = sigmoid(self.bias)

class Net:
    """
    The big nets class
    """
    def __init__(self):
        self.nodes = np.empty(settings.max_layers+1, dtype=object)
        self.fitness = None
        #Randomly fill out the net as specified in the settings file
        for i in range(len(self.nodes)):
            self.nodes[i] = np.empty(0)

        for _ in range(settings.input_nodes):
            self.nodes[0] = np.append(self.nodes[0], Node(self))

        for _ in range(settings.output_nodes):
            bias = 2*np.random.rand()-1
            self.nodes[-1] = np.append(self.nodes[-1], Node(self, bias))

        for _ in range(np.random.randint(settings.initial_nodes)):
            bias = 2*np.random.rand()-1
            self.add_random_node(bias)

        for _ in range(np.random.randint(settings.initial_links)):
            bias = 2*np.random.rand()-1
            self.add_random_link(bias)

    def output(self, inputs):
        """
        Uses the inputs as the biases for the input nodes
        Then moves through the hidden layers, updaing all nodes in each layer
        Finally returns the outputs from the output layer nodes
        """
        for i, inp in enumerate(inputs):
            self.nodes[0][i].bias = inp
        for layer in self.nodes:
            for node in layer:
                node._output()
        return [node.output for node in self.nodes[-1]]

    def mutate(self, temperature):
        """
        Perform the mutations based on the GNARL laerning algorithm
        """
        self.fitness = None
        instant_temperature = temperature*np.random.random()
        std_dev = instant_temperature*settings.proportionality
        for layer in self.nodes[1:]:
            for node in layer:
                node.mutate(std_dev)
        link_change = np.random.randint(settings.max_link_change*instant_temperature+1) + settings.min_link_change
        node_change = np.random.randint(settings.max_node_change*instant_temperature+1) + settings.min_node_change
        for _ in range(link_change):
            add = random.getrandbits(1)
            if add:
                self.add_random_link()
            else:
                self.remove_random_link()
        for _ in range(node_change):
            add = random.getrandbits(1)
            if add:
                self.add_random_node()
            else:
                self.remove_random_node()
        self.clear()

    def clear(self):
        """
        Resets all nodes to their bias values, removing memories
        """
        for layer in self.nodes:
            for node in layer:
                node.clear()

    def add_random_node(self, bias=0):
        """
        Adds a node to a random layer
        """
        layer = np.random.choice(range(1,settings.max_layers))
        self.nodes[layer] = np.append(self.nodes[layer], Node(self, bias))

    def add_random_link(self, bias=0):
        """
        Adds a random link based on GNARL algorithm
        """
        #decide which layer will take the link as input
        start_choice_weights = np.empty(settings.max_layers+1)
        #fill an array with the number of potential start nodes per layer
        start_choice_weights[0] = 0
        for i in range(settings.max_layers-1):
            start_choice_weights[1:-1][i] = len(self.nodes[1:-1][i])
        start_choice_weights[-1] = settings.output_nodes
        #remove nodes that have all connections fulfilled
        for layer in range(1, len(self.nodes)):
            cut_nodes = np.delete(self.nodes, layer)
            max_possible = sum(len(l) for l in cut_nodes)
            if layer < settings.max_layers:
                max_possible += 1-settings.output_nodes
            for node in range(len(self.nodes[layer])):
                if len(self.nodes[layer][node].links) >= max_possible:
                    start_choice_weights[layer] -= 1
        sum_scw = sum(start_choice_weights[1:-1])
        if start_choice_weights[-1] == 0:
            if sum_scw != 0:
                start_choice_weights[1:-1] /= sum_scw
            else:
                #print("Warning: There are no more valid link locations in this net")
                return None
        else:
            if sum_scw == 0:
                start_choice_weights[-1] = 1.
            else:
                start_choice_weights[1:-1] *= settings.regular_layer_bias/sum_scw
                start_choice_weights[-1] = settings.in_out_layer_bias
        #select the layer
        start_layer = np.random.choice(range(settings.max_layers+1), p=start_choice_weights)
        #find the viable starts from this layer and select
        cut_nodes = np.delete(self.nodes, start_layer)
        max_possible = sum(len(l) for l in cut_nodes)
        if start_layer < settings.max_layers:
            max_possible += 1-settings.output_nodes
        start_node_allowed = np.array([1. if len(node.links)<max_possible else 0. for node in self.nodes[start_layer]])
        start_node_allowed /= sum(start_node_allowed)
        start_node_number = np.random.choice(range(len(self.nodes[start_layer])), p=start_node_allowed)
        start_node = self.nodes[start_layer][start_node_number]
        #decide where the link takes output from
        end_choice_weights = np.empty(settings.max_layers+1)
        #fill array with number of pottential nodes it could link to
        for i in range(settings.max_layers-1):
            if i+1 == start_layer:
                end_choice_weights[1:-1][i] = 1
            else:
                end_choice_weights[1:-1][i] = len(self.nodes[1:-1][i])
        input_connections = 0
        #remove nodes it has already linked to from the potential node array
        for link in start_node.links:
            connection = link.connection[0]
            if connection != 0:
                end_choice_weights[connection] -= 1
            else:
                #calculate the number of times connected to input node
                #important so that the biassing can work
                input_connections += 1

        sum_ecw = sum(end_choice_weights[1:-1])
        #If all input nodes are connected to, normalise over the rest of the nodes
        #Assumes the start node has been selected as valid
        if input_connections == settings.input_nodes:
            end_choice_weights[1:-1] /= sum_ecw
            end_choice_weights[0] = 0
        #Otherwise normalise over all nodes and bias to input nodes.
        else:
            if sum_ecw != 0:
                end_choice_weights[1:-1] *= settings.regular_layer_bias/sum_ecw
                end_choice_weights[0] = 1-sum(end_choice_weights[1:-1])#settings.in_out_layer_bias
            else:
                end_choice_weights[0] = 1
        end_choice_weights[-1] = 0
        end_layer = np.random.choice(range(settings.max_layers+1), p=end_choice_weights)
        if start_layer == end_layer:
            end_node_number =  start_node_number
        else:
            probs = np.array([1. for _ in range(len(self.nodes[end_layer]))])
            for link in start_node.links:
                connection = link.connection
                if connection[0] == end_layer:
                    probs[connection[1]] = 0.
            probs /= sum(probs)
            end_node_number = np.random.choice(range(len(self.nodes[end_layer])), p=probs)
        start_node.add_link((end_layer, end_node_number), bias)

    def remove_random_node(self):
        """
        Delete a random node from the hidden layer
        """
        layer_weights = np.empty(len(self.nodes))
        layer_weights[0] = 0.
        for i,layer in enumerate(self.nodes[1:-1]):
            layer_weights[i+1] = len(layer)
        layer_weights[-1] = 0.
        sum_lw = sum(layer_weights)
        if sum_lw != 0:
            layer_weights /= sum_lw
        else:
            #print("Warning: There are no hidden nodes to delete")
            return None
        layer_num = np.random.choice(range(len(self.nodes)), p=layer_weights)
        node_num = np.random.choice(range(len(self.nodes[layer_num])))
        self.nodes[layer_num] = np.delete(self.nodes[layer_num], node_num)
        for layer in self.nodes[1:]:
            for node in layer:
                for l, link in enumerate(node.links):
                    if link.connection == (layer_num, node_num):
                        node.links = np.delete(node.links, l)
                    elif link.connection[0] == layer_num:
                        if link.connection[1] > node_num:
                            link.connection = (link.connection[0], link.connection[1]-1)

    def remove_random_link(self):
        """
        Delete a random  link from the hidden layer based on GNARL algorithm
        """
        #decide which layer to remove link from
        start_choice_weights = np.empty(settings.max_layers+1, dtype=object)
        #fill an array with the number of links in each layer
        start_choice_weights[0] = [0.]
        for i in range(settings.max_layers):
            count = np.array([len(node.links) for node in self.nodes[1:][i]])
            start_choice_weights[1:][i] = count
        sum_weights = np.array([sum(x) for x in start_choice_weights])
        sum_scw = sum(sum_weights[1:-1])
        if sum_weights[-1] == 0:
            if sum_scw != 0:
                sum_weights[1:-1] /= sum_scw
            else:
                #print("Warning: There are no links to delete")
                return None
        else:
            if sum_scw != 0:
                sum_weights[1:-1] *= settings.regular_layer_bias/sum_scw
                sum_weights[-1] = settings.in_out_layer_bias
            else:
                sum_weights[-1] = 1.

        layer = np.random.choice(range(len(self.nodes)), p=sum_weights)
        layer_nodes = self.nodes[layer]
        layer_weights = start_choice_weights[layer]/sum(start_choice_weights[layer])
        node = np.random.choice(layer_nodes, p=layer_weights)
        link = np.random.choice(range(len(node.links)))
        node.links = np.delete(node.links, link)
