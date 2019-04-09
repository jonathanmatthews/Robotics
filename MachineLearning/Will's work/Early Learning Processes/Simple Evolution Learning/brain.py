# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 16:38:02 2019

@author: William
"""

import numpy as np
from sigmoid import sigmoid
from config import Config
from rand_range import rand_range

settings = Config()

class Brain():
    def __init__(self, size=None, weights=None, bias=None, output_type="cont", w_rates=None, b_rates=None):
        if output_type in ["cont", "disc"]:
            self._type = output_type
        else:
            raise ValueError("output_type must be 'cont' or 'disc' not {}".format(output_type))

        if bias != None:
            self.bias = bias
        else:
            self.bias = [np.zeros(size[0])]
            self.bias = np.array(self.bias + [np.random.randn(s) for s in size[1:]])

        if weights != None:
            self.weights = weights
        else:
            self.weights = [None]
            for previous_layer, neuron_count in enumerate(size[1:]):
                self.weights.append(np.array([np.random.randn(size[previous_layer]) for _ in range(neuron_count)]))
            self.weights = np.array(self.weights)

        if w_rates != None:
            self.w_rates = w_rates
        else:
            self.w_rates = [None]
            for previous_layer, neuron_count in enumerate(size[1:]):
                self.w_rates.append(np.array([np.zeros(size[previous_layer])+settings.initial_rate for _ in range(neuron_count)]))
            self.w_rates = np.array(self.w_rates)

        if b_rates != None:
            self.b_rates = b_rates
        else:
            self.b_rates = [np.zeros(size[0])]
            self.b_rates = np.array(self.b_rates + [np.zeros(s)+settings.initial_rate for s in size[1:]])
        self.fitness = 0.0

    def output(self, inputs):
        outputs = inputs
        for layer in range(1, len(self.weights)):
            outputs=[sigmoid(np.sum(outputs*self.weights[layer][neuron])+self.bias[layer][neuron]) for neuron in range(len(self.weights[layer]))]

        if self._type == 'cont':
            return [(output*settings.output_range)+settings.output_min for output in outputs]
        elif self._type == 'disc':
            return outputs.index(max(outputs))
        else:
            raise ValueError("output_type must be 'cont' or 'disc' not {}".format(self._type))

    def calc_fitness(self, env, output_range, max_steps, repeats):
        fitnesses = [0.0 for _ in range(repeats)]
        for r in range(repeats):
            observation = env.reset()
            for t in range(max_steps):
                action = self.output(observation)
                observation, reward, done, info = env.step(np.array(action))
                fitnesses[r] += reward
                if done:
                    break
        self.fitness = sum(fitnesses)/repeats
        env.close()
        return self.fitness

    def mutate(self):
        for i in range(1, len(self.weights[1:])+1):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    self.weights[i][j][k] += rand_range(-self.w_rates[i][j][k], self.w_rates[i][j][k])
                    self.w_rates[i][j][k] += rand_range(-settings.settle_rate, settings.settle_rate)

        for i in range(1, len(self.bias[1:])+1):
            for j in range(len(self.bias[i])):
                self.bias[i][j] += rand_range(-self.b_rates[i][j], self.b_rates[i][j])
                self.b_rates[i][j] += rand_range(-settings.settle_rate, settings.settle_rate)

    def __repr__(self):
        return "Brain(weights={}, bias={}, output_type={}, w_rates={}, b_rates={})".format(repr(self.weights), repr(self.bias), repr(self._type), repr(self.w_rates), repr(self.b_rates))


