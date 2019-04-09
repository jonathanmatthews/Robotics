class Config:
    def __init__(self):
        #brain
        self.number_inputs = 4
        self.neurons_per_layer = 30
        self.number_layers = 5

        #neuron
        self.bias_range = 2
        self.min_bias = -1

        #axon
        self.weight_range = 2
        self.min_weight = -1

        #mutating
        self.initial_rate = 0.1

        #learning
        self.number_brains = 100
        self.base_weight = 0