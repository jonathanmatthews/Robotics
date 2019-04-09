import random
from config import Config

settings = Config()

class Axon():
    def __init__(self, input_neuron, weight = None):
        self.mutation_rate = settings.initial_rate
        if weight == None:
            self.weight = random.random()*settings.weight_range+settings.min_weight
        else:
            self.weight = weight
        self.input_neuron = input_neuron

    def calculate(self):
        output = self.input_neuron.output*self.weight
        return output

    def mutate(self):
        self.weight += (random.random()*self.mutation_rate*2)-self.mutation_rate