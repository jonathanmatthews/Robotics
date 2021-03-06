# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:30:16 2019

Works in python 2

@author: William
"""
import numpy as np
from neural_net import neural_net


def sigmoid(inp):
    """
    Just a really useful sigmoid function
    """
    output = 1/(1 + float(np.exp(-inp)))
    return output


class Link:
    """
    Link class for python 2
    """

    def __init__(self, net, connection, weight):
        self.net = net
        self.connection = connection  # tuple of (layer, specific)
        self.weight = weight

    def output(self):
        """
        Checks it's input node and recalculates it's output
        """
        return self.weight*self.net.nodes[self.connection[0]][self.connection[1]].output


class Node:
    """
    Node class for python 2
    """

    def __init__(self, net, bias, links):
        self.net = net
        self.bias = bias
        self.links = np.array([], dtype=object)
        for link_info in links:
            self.links = np.append(self.links, Link(
                net, link_info[0], link_info[1]))
        self.output = None
        self.clear()

    def _output(self):
        """
        Updates all its links then recalculates it's output
        """
        total = sum(link.output() for link in self.links)
        total += self.bias
        self.output = sigmoid(total)

    def clear(self):
        """
        Recalculates the output with no links.
        Removes 'memories' from back links
        """
        self.output = sigmoid(self.bias)

    def __repr__(self):
        """
        A really ugly, barely useful representation of the node
        """
        strng = "Node(bias={},links=".format(self.bias)
        for link in self.links:
            strng += "(weight={},connection={})".format(link.weight,
                                                        link.connection)
        strng += ")"
        return strng


class Net:
    """
    Net class for python 2. Intialise by pointing to a net_data, txt file
    generated be conver_pkl
    """

    def __init__(self):
        """
        Reads from the provided file to generate the net as it was in python 3
        """
        layers = neural_net['Net']
        layer_count = len(layers)
        layer_index = 0
        layer_values = np.empty(0, dtype=object)
        self.nodes = np.empty(layer_count, dtype=object)


        for layer_index, layer in enumerate(layers):
            nodes = layer['Layer']
            for node in nodes:
                node_dictionary = node['Node']
                # print node_dictionary
                bias = node_dictionary['bias']
                links = node_dictionary['links']

                formatted_links = [((int(dictionary['connection'][0]), int(dictionary['connection']
                                     [1])), dictionary['weight']) for dictionary in links]

                # print bias, formatted_links
                node = Node(self, bias, formatted_links)
                layer_values = np.append(layer_values, node)
            self.nodes[layer_index] = layer_values
            layer_values = np.empty(0, dtype=object)

    def output(self, inputs):
        """
        Performs the same as the python 3 classs
        Uses the inputs as the biases for the input nodes
        Then moves through the hidden layers, updaing all nodes in each layer
        Finally returns the outputs from the output layer nodes

        Second number is lean back, first is lean forward
        """
        for i, inp in enumerate(inputs):
            self.nodes[0][i].bias = inp
        for layer in self.nodes:
            for node in layer:
                node._output()
        return [node.output for node in self.nodes[-1]]




