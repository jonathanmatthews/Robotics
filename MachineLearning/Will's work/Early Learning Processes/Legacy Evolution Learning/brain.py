from config import Config
import numpy as np
from neuron import Neuron
from input_neuron import Input

settings = Config()

class Brain():
    def __init__(self, inputs = None, weights = None):
        self.neuron_array = np.empty([settings.number_layers, settings.neurons_per_layer], dtype = object)
        self.weights = np.empty([(settings.number_layers * settings.neurons_per_layer) + 1], dtype = object)
        #self.fitness = 0
        if inputs is None:
            inputs = np.zeros([settings.number_inputs])

        for layer in range(settings.number_layers):
            if layer == 0:
                layer_inputs = np.empty(len(inputs), dtype = object)
                for i in range (len(inputs)):
                    layer_inputs[i] = Input(inputs[i])
                self.brain_inputs = layer_inputs
            else:
                layer_inputs = self.neuron_array[layer - 1]

            if weights is None:
                for neuron in range (settings.neurons_per_layer):
                    self.neuron_array[layer, neuron] = Neuron(layer_inputs)
            else:
                for neuron in range (settings.neurons_per_layer):
                    self.neuron_array[layer, neuron] = Neuron(layer_inputs, weights[layer*settings.neurons_per_layer+neuron])

        if weights is None:
            self.output_neuron = Neuron(self.neuron_array[-1])
            self.output = self.output_neuron.output
            self.save()

        else:
            self.output_neuron = Neuron(self.neuron_array[-1], weights[-1])
            self.output = self.output_neuron.output
            self.save()

    def update(self, values):
        for i,v in enumerate(values):
            self.brain_inputs[i].output = v
        for layer in range (settings.number_layers):
            for neuron in range (settings.neurons_per_layer):
                self.neuron_array[layer, neuron].update()
        self.output_neuron.update()
        self.output = self.output_neuron.output

    def save(self):
        for layer in range (settings.number_layers):
            for neuron in range (settings.neurons_per_layer):
                self.neuron_array[layer, neuron].save()
                self.weights[layer*settings.neurons_per_layer+neuron] = self.neuron_array[layer, neuron].weights
        self.output_neuron.save()
        self.weights[-1] = self.output_neuron.weights

    def load(self, weights):
        for layer in range (settings.number_layers):
            for neuron in range (settings.neurons_per_layer):
                self.neuron_array[layer, neuron].load(weights[layer*settings.neurons_per_layer+neuron])

        self.output_neuron.load(weights[-1])
        self.output = self.output_neuron.output
        self.save()

    def mutate(self):
        for layer in range (settings.number_layers):
            for neuron in range (settings.neurons_per_layer):
                self.neuron_array[layer, neuron].mutate()
        self.output_neuron.mutate()
        self.save()
