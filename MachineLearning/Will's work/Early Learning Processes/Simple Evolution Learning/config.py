class Config:
    def __init__(self):
        #brain
        self.brain_format = [6, 30, 30, 30, 30, 30, 3]
        self.env_name = "CartPole-v1"
        self.output_type = "disc"
        self.output_range = 4
        self.output_min = -2

        #mutating
        self.initial_rate = 0.1
        self.settle_rate = 0.03

        #Acrobot-v1#92#Pendulum-v0#56to cart-pole-v1#39#37#34#0
        #learning
        self.number_brains = 100#100#40#50#100#100
        self.max_steps = 200#500#300#1200#12000#3600#2400#1200
        self.fitness_repeats = 1#3#5#2#1#1#1#4
        self.base_weight = 0
        self.save_rate = 5

        #visualisation
        self.vis_steps = 10000