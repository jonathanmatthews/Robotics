# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:18:18 2019

@author: William
"""
import pickle
import numpy as np
from typing import Dict
import json

def save_json(data: Dict, file_to_save='neural_net.json') -> None:
    """
    Saves dictionary to json file
    Args:
        data: dictionary containing neural net
        file_to_save: name of file to save as
    Returns:
        None
    """
    with open(file_to_save, 'w') as output_file:
        json.dump(data, output_file, indent=4)

nets = []
file = open("net_python3.pkl", "rb")
while True:
    try:
        nets.append(pickle.load(file))
    except EOFError:
        break
file.close()

nets = np.array(nets)
net_fits = np.array([net.fitness for net in nets])

net = nets[np.argmax(net_fits)]
print(net.nodes)

output_net = []

for i, layer in enumerate(net.nodes):
    layer_data = []
    for j, node in enumerate(layer):
        node_data = {
            'bias': float(node.bias),
        }
        node_links_data = []
        for link in node.links:
            node_links_data.append({
                'weight': float(link.weight),
                'connection': [float(link.connection[0]), float(link.connection[1])]
            })
        node_data['links'] = node_links_data

        layer_data.append({
            'Node': node_data  
        })
    output_net.append({
        'Layer': layer_data
    })
final_dict = {
    'Net': output_net
}


save_json(final_dict)
