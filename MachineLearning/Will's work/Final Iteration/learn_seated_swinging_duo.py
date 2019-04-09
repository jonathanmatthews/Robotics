# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:52:58 2019

Run simulaiion required to find fitness then delete and evolve as required.

@author: William
"""

from network import Net
import settings
import numpy as np
import pickle
import signal
import copy
import os

import Seated_Stiff as SSwingEnv

running = True
def signal_handler(signal, frame):
    """
    Allows the program to be terminated at a sensible position in the code.
    """
    global running
    if running:
        print("\nFinishing loop then Ending\n")
        running = False
    else:
        raise ValueError("Double Interupt Detected. Crashing program out. Latest Generation unsaved.")
signal.signal(signal.SIGINT, signal_handler)

def load_gen():
    """
    Chec the save path for the oldest generation then load all available nets
    """
    save_path = os.path.join(os.getcwd(),"SSwingEnv")
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
    """
    Save all nets and fitnesses to the save path
    """
    print("Beginning save of generation {}...".format(generation))
    file_path = os.path.join(save_path, "Generation {}.pkl".format(generation))
    with open(file_path, 'wb') as file:
        for net in nets:
            pickle.dump(net, file)

def run_gen(nets, generation, oldest_gen, save_path, force, first):
    """
    Learn for one generation
    """
    print("Generation: {}, Self Start: {}".format(generation,not force))
    #Find fitnesses of nets without saved fitnesses
    net_fitnesses = np.empty(settings.number_nets)
    if force:
        max_steps = settings.max_steps_pre_start
        max_fitness = settings.max_fitness_pre_start
    else:
        max_steps = settings.max_steps_self_start
        max_fitness = settings.max_fitness_self_start
    for n, net in enumerate(nets):
        print("\b\b\b\b{:.0f}%".format(n), end="\r")
        if net.fitness == None or first:
            fitnesses = [0. for _ in range(settings.repeats)]
            for r in range(settings.repeats):
                env = SSwingEnv.initialise(force)
                observation, env = SSwingEnv.stepper(*env, 0)
                for t in range(max_steps):
                    output = net.output(observation)
                    action = [output[:2].index(max(output[:2])), output[2:].index(max(output[2:]))]
                    prev_vel = observation[1]
                    observation, env = SSwingEnv.stepper(*env, action)
                    reward = abs(observation[0]+0.009)
                    if force:
                        reward = abs(observation[0])
                    else:
                        if prev_vel*observation[1] < 0:
                            if observation[1] < 0:
                                reward = abs(observation[0])
                            else:
                                reward = -abs(observation[0])
                    fitnesses[r] += reward
            net.fitness = sum(fitnesses)/settings.repeats
        net_fitnesses[n] = net.fitness
    max_fit = max(net_fitnesses)
    min_fit = min(net_fitnesses)
    #Print Progress
    print("\b\b\b\bMaximum fitness:", max_fit,
          "with net:", np.argmax(net_fitnesses),
          "\nMinimum fitness:", min_fit,
          "with net:", np.argmin(net_fitnesses),
          "\nAverage fitness:", sum(net_fitnesses)/settings.number_nets,
          "\n")

    #Save if told to finish or at regular intervals
    if not running:
        save(nets, generation, save_path)
        return None

    if generation%settings.save_rate == 0:
        if generation != oldest_gen or generation == 0:
            save(nets, generation, save_path)


    print("Selecting Parent Nets")
    #Selection algoithms based on fitnesses to take best 25 nets and a selection of other 25
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

    print("Beginning Repopulation")
    #copy nets and then mutate them to form new nets
    new_nets = np.array([copy.deepcopy(net) for net in parent_nets])
    net_temps = [1-net.fitness/(max_fitness) for net in new_nets]
    for new_net, net_temp in zip(new_nets, net_temps):
        new_net.mutate(net_temp)
    nets = np.append(parent_nets, new_nets)
    print("Generation {} finished\n".format(generation))
    return nets

#Run loop
nets, oldest_gen, save_path = load_gen()
generation = oldest_gen
force = True
while True:
    old_force = force
    if generation%settings.gens_per_cycle < settings.gens_pre_start:
        force = True
    else:
        force = False
    if old_force != force:
        first = True
    elif oldest_gen == generation:
        first = True
    else:
        first = False
    nets = run_gen(nets, generation, oldest_gen, save_path, force, first)
    if nets is None:
        break
    generation += 1
