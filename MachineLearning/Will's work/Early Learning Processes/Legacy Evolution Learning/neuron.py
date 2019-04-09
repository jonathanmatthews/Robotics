import random
import sigmoid
from config import Config
import numpy as np
from axon import Axon

settings = Config()

class Neuron():
    def __init__(self, input_neurons, weights = None):
        self.weights = np.empty(len(input_neurons)+1)
        self.axons = np.empty([0])
        self.output = 0
        for i in range (len(input_neurons)):
            if weights is None:
                axon = Axon(input_neurons[i])
            else:
                axon = Axon(input_neurons[i], weights[i])
            self.axons = np.append(self.axons, axon)
        if weights is None:
            self.bias = -(random.random()*settings.bias_range + settings.min_bias)
        else:
            self.bias = weights[-1]
        self.mutation_rate = settings.initial_rate
        self.update()
        self.save()

    def update(self):
        activation = 0
        for n in range (len(self.axons)):
            activation += self.axons[n].calculate()
        activation += self.bias
        self.output = sigmoid.sigmoid(activation)

    def save(self):
        for i in range (len(self.axons)):
            self.weights[i] = self.axons[i].weight
        self.weights[-1] = self.bias

    def load(self, weights):
        for i in range (len(self.axons)):
            self.axons[i].weight = weights[i]
        self.bias = weights[-1]
        self.update()
        self.save()

    def mutate(self):
        for axon in self.axons:
            axon.mutate()
        self.bias += (random.random()*self.mutation_rate*2)-self.mutation_rate