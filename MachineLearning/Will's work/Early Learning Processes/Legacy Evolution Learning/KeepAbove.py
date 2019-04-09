# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:38:20 2019

@author: William
"""
import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from config import Config

settings = Config()

class KeepAbove():
    def __init__(self):
        self.tau = settings.tau
        self.x = 0.0
        self.v = 0.0
        self.target = 0.0
        self.deviation = settings.deviation

        self.steps_beyond_done = None

        ################  failure  , x too large
        high = np.array([self.deviation, np.finfo(np.float32).max])
        low = -high

        self.action_space = spaces.Box(np.array([np.finfo(np.float32).min]), np.array([np.finfo(np.float32).max]), dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def step(self, action):

        self.target += math.sin(self.t)
        error = self.x - self.target
        done = not self.observation_space.contains(np.array([error,action]))

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array([error, self.x, self.t]), reward, done, {}

    def reset(self):
        self.target = 0.0
        self.x = 0.0
        self.t = 0.0
        self.steps_beyond_done = None
        return np.array([0,0,0])

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self):
        print("{:.2f}\t{:.9}\t{:.9}".format(self.t, self.x, math.sin(self.t)))

env = KeepAbove()

states = 1000

Q = np.zeros([states, env.action_space.shape[0]])

for i_episode in range(20):
    observation = env.reset()
    for t in range(states):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            env.render()
            print("Episode {} completed for {} timesteps".format(i_episode+1, t+1))
            break