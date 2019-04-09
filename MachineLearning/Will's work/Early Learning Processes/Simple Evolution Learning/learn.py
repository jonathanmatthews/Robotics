# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:52:58 2019

@author: William
"""

from brain import Brain
from config import Config
import gym
import numpy as np
from numpy import array #analysis:ignore
import signal
import copy
import os

from premade_acrobot import AcrobotEnv

settings = Config()

def signal_handler(signal, frame):
    global running
    if running:
        print("Finishing loop then Ending\n")
        running = False
    else:
        raise ValueError("Double Interupt Detected. Crashing program out. Latest Generation may need deleting.")
signal.signal(signal.SIGINT, signal_handler)

save_path = os.path.join(os.getcwd(),settings.env_name)
if not os.path.exists(save_path):
    os.makedirs(save_path)

try:
    oldest_gen = max([int(x.split(" ")[1]) for x in os.listdir(save_path)])
except ValueError:
    oldest_gen = 0
oldest_str = "Generation "+str(oldest_gen)
gen_path = os.path.join(save_path, oldest_str)
if not os.path.exists(save_path):
    os.makedirs(save_path)

if oldest_gen != 0:
    nets = os.listdir(gen_path)
    net_fits = np.array([float(x.split(" ")[-1].split(".")[0]) for x in nets])
    sum_net_fits = sum(net_fits)
    if sum_net_fits == 0:
        probs = None
    else:
        probs = [fit/sum_net_fits for fit in  net_fits]

    try:
        brain_paths = np.random.choice(nets, settings.number_brains, False, probs)
    except:
        print("Insufficient Brain count. Taking Random Sample")
        brain_paths = np.random.choice(nets, settings.number_brains, True, probs)

    brains = np.array([], dtype=object)
    for brain_path in brain_paths:
        path = os.path.join(gen_path, brain_path)
        with open(path, "r") as file:
            file_string = ""
            for line in file:
                file_string += line
            brain = eval(file_string)
            brains = np.append(brains, brain)
else:
    brains = np.array([Brain(settings.brain_format, output_type=settings.output_type) for _ in range(settings.number_brains)])

env = AcrobotEnv()
#env = gym.make(settings.env_name)
#env._max_episode_steps = settings.max_steps+1
running = True

for generation in range(oldest_gen, 1000+oldest_gen):
    fitnesses = np.array([brain.calc_fitness(env, settings.output_range, settings.max_steps, settings.fitness_repeats) for brain in brains])
    max_fit = max(fitnesses)
    min_fit = min(fitnesses)
    print("Generation:", generation,
          "\nMaximum fitness:", max_fit,
          "with brain:", np.argmax(fitnesses),
          "\nMinimum fitness:", min_fit,
          "with brain:", np.argmin(fitnesses),
          "\nAverage fitness:", sum(fitnesses)/settings.number_brains,
          "\n")

    if not running:
        print("Beginning save of generation {}...".format(generation))
        folder_path = os.path.join(save_path, "Generation {}".format(generation))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for i, brain in enumerate(brains):
            file_path = os.path.join(folder_path, "network {} fitness {}.txt".format(i, brain.fitness))
            with open(file_path, 'w') as file:
                file.writelines(repr(brain))
        print("Save finished\n")
        break

    if generation%settings.save_rate == 0 and generation != oldest_gen:
        print("Beginning save of generation {}...".format(generation))
        folder_path = os.path.join(save_path, "Generation {}".format(generation))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for i, brain in enumerate(brains):
            file_path = os.path.join(folder_path, "network {} fitness {}.txt".format(i, brain.fitness))
            with open(file_path, 'w') as file:
                file.writelines(repr(brain))
        print("Save finished\n")

    weightings = fitnesses-min_fit
    weight_sum = sum(weightings)
    if weight_sum == 0:
        probs = np.array([1/len(brains) for _ in range(len(brains))])
    else:
        probs = weightings/weight_sum

    try:
        brains = np.random.choice(brains, int(settings.number_brains/2), False, probs)
    except ValueError:
        brains = np.random.choice(brains, int(settings.number_brains/2), True, probs)
        brains = [copy.deepcopy(brain) for brain in brains]

    new_brains = [copy.deepcopy(brain) for brain in brains]
    for new_brain in new_brains:
        new_brain.mutate()
    brains = np.append(brains, new_brains)
