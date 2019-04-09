# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:52:58 2019

@author: William
"""

from network import Net
import settings
import numpy as np
import pickle
import signal
import copy
import os

import Parametric_Swinging_ML_Will as PSwingEnv

running = True
def signal_handler(signal, frame):
    global running
    if running:
        print("Finishing loop then Ending\n")
        running = False
    else:
        raise ValueError("Double Interupt Detected. Crashing program out. Latest Generation may need deleting.")
signal.signal(signal.SIGINT, signal_handler)

def load_gen():
    save_path = os.path.join(os.getcwd(),"PSwingEnv")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    try:
        oldest_gen = max([int(x.split(" ")[1].strip(".pkljg")) for x in os.listdir(save_path)])
    except ValueError:
        oldest_gen = 0
    oldest_str = "Generation "+str(oldest_gen)+".pkl"
    gen_path = os.path.join(save_path, oldest_str)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if oldest_gen != 0:
        nets = []
        file = open(gen_path, "rb")
        while True:
            try:
                nets.append(pickle.load(file))
            except EOFError:
                break
        file.close()
    #    if sum_net_fits == 0:
    #        probs = None
    #    else:
    #        probs = [fit/sum_net_fits for fit in  net_fits]
        nets = np.array(nets)
        try:
            nets = np.random.choice(nets, settings.number_nets, False)
        except:
            print("Insufficient saved nets. Taking Random Sample")
            nets = np.random.choice(nets, settings.number_nets, True)
    else:
        nets = np.array([Net() for _ in range(settings.number_nets)])
    return nets, oldest_gen, save_path

def save(nets, generation, save_path):
    print("Beginning save of generation {}...".format(generation))
    file_path = os.path.join(save_path, "Generation {}.pkl".format(generation))
    with open(file_path, 'wb') as file:
        for net in nets:
            pickle.dump(net, file)
    print("Save finished\n")

def run_gen(nets, generation, oldest_gen, save_path):
    net_fitnesses = np.empty(settings.number_nets)
    for n, net in enumerate(nets):
        if net.fitness == None:
            fitnesses = [0. for _ in range(settings.repeats)]
            for r in range(settings.repeats):
                env = PSwingEnv.initialise()
                observation, env = PSwingEnv.stepper(*env, 0)
                for t in range(settings.max_steps):
                    output = net.output(observation)
                    action = output.index(max(output))
                    observation, env = PSwingEnv.stepper(*env, action)
                    reward = abs(observation[0])
                    fitnesses[r] += reward
            net.fitness = sum(fitnesses)/settings.repeats
        net_fitnesses[n] = net.fitness
    max_fit = max(net_fitnesses)
    min_fit = min(net_fitnesses)
    print("Generation:", generation,
          "\nMaximum fitness:", max_fit,
          "with net:", np.argmax(net_fitnesses),
          "\nMinimum fitness:", min_fit,
          "with net:", np.argmin(net_fitnesses),
          "\nAverage fitness:", sum(net_fitnesses)/settings.number_nets,
          "\n")

    if not running:
        save(nets, generation, save_path)
        return None

    if generation%settings.save_rate == 0:
        if generation != oldest_gen or generation == 0:
            save(nets, generation, save_path)

    weightings = net_fitnesses-min_fit

    parent_nets = np.empty(int(settings.number_nets/2), dtype=object)
    for i in range(settings.certain_parents):
        index = np.argmax(weightings)
        parent_nets[i] = nets[index]
        nets = np.delete(nets, index)
        weightings = np.delete(weightings, index)

    weight_sum = sum(weightings)
    if weight_sum == 0:
        probs = np.array([1/len(nets) for _ in range(len(nets))])
    else:
        probs = weightings/weight_sum

    try:
        parent_nets[i+1:] = np.random.choice(nets, settings.random_parents, False, probs)
    except ValueError:
        parent_nets[i+1:] = np.random.choice(nets, settings.random_parents, True, probs)
        parent_nets = np.array([copy.deepcopy(net) for net in parent_nets])

    new_nets = np.array([copy.deepcopy(net) for net in parent_nets])
    net_temps = [1-net.fitness/(settings.max_fitness) for net in new_nets]
    for new_net, net_temp in zip(new_nets, net_temps):
        new_net.mutate(net_temp)
    nets = np.append(parent_nets, new_nets)
    return nets

nets, oldest_gen, save_path = load_gen()
generation = oldest_gen
while True:
    nets = run_gen(nets, generation, oldest_gen, save_path)
    if nets is None:
        break
    generation += 1

