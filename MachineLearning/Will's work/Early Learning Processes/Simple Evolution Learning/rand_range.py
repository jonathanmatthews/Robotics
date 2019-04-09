# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:32:37 2019

@author: William
"""
import random

def rand_range(mini, maxi):
    ret = random.random()
    ret *= maxi-mini
    ret += mini
    return ret
