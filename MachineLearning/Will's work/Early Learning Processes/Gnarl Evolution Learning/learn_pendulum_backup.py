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

import gym

running = True
def signal_handler(signal, frame):
    global running
    if running:
        print("Finishing loop then Ending\n")
        running = False
    else:
        raise ValueError("Double Interupt Detected. Crashing program out. Latest Generation may need deleting.")
signal.signal(signal.SIGINT, signal_handler)

save_path = os.path.join(os.getcwd(),"PendulumEnv")
if not os.path.exists(save_path):
    os.makedirs(save_path)

try:
    oldest_gen = max([int(x.split(" ")[1].strip(".pkl")) for x in os.listdir(save_path)])
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

env = gym.make('Pendulum-v0')
env._max_episode_steps = settings.max_steps*2

def save(nets, generation):
    print("Beginning save of generation {}...".format(generation))
    file_path = os.path.join(save_path, "Generation {}.pkl".format(generation))
    with open(file_path, 'wb') as file:
        for net in nets:
            pickle.dump(net, file)
    print("Save finished\n")

def run_gen(nets, generation):
    net_fitnesses = np.empty(settings.number_nets)
    for n, net in enumerate(nets):
        fitnesses = [0. for _ in range(settings.repeats)]
        for r in range(settings.repeats):
            observation = env.reset()
            for t in range(settings.max_steps):
                output = net.output(observation)
                action = 4*output[0]-2
                observation, reward, done, info = env.step(np.array([action]))
                fitnesses[r] += reward
                if done:
                    break
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
        save(nets, generation)
        return None

    if generation%settings.save_rate == 0 and generation != oldest_gen:
        save(nets, generation)

    weightings = net_fitnesses-min_fit
    weight_sum = sum(weightings)
    if weight_sum == 0:
        probs = np.array([1/len(nets) for _ in range(len(nets))])
    else:
        probs = weightings/weight_sum

    try:
        nets = np.random.choice(nets, int(settings.number_nets/2), False, probs)
    except ValueError:
        nets = np.random.choice(nets, int(settings.number_nets/2), True, probs)
        nets = np.array([copy.deepcopy(net) for net in nets])

    new_nets = np.array([copy.deepcopy(net) for net in nets])
    net_temps = [-net.fitness/(16.27360440*settings.max_steps) for net in new_nets]
    for new_net, net_temp in zip(new_nets, net_temps):
        new_net.mutate(net_temp)
    nets = np.append(nets, new_nets)
    return nets

for generation in range(oldest_gen, 1000+oldest_gen):
    nets = run_gen(nets, generation)
    if nets is None:
        break

