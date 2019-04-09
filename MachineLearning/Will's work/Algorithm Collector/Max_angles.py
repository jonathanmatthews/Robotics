# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:33:25 2019

@author: William
"""
import pandas as pd
import matplotlib.pyplot as plt


algorithm_types = ["Testing_Algorithm", "Evolution", "QLearning"]

dfs = {}
for typ in algorithm_types:
    file_name = typ +"_data.csv"
    df = pd.read_csv(file_name, names=["Times", "Angles"])
    dfs[typ] = df

times = {}
max_angles = {}
for index in dfs:
    times[index] = dfs[index].Times
    if index == "QLearning":
        times[index] += 43
    max_angles[index] = []
    angles = dfs[index].Angles
    for angle in angles:
        try:
            if max_angles[index][-1] < abs(angle):
                max_angles[index].append(abs(angle))
            else:
                max_angles[index].append(max_angles[index][-1])
        except IndexError:
            max_angles[index].append(0)

plt.figure()
for index in dfs:
    plt.plot(times[index], max_angles[index], label=index)
plt.plot([0,43], [0,0], "#2ca02c")
plt.xlim(0, 1000)
plt.xlabel("Time/s")
plt.ylabel("Angle/deg")
#plt.title("Swing Amplitude over time for generation {}".format(oldest_gen))
plt.legend()
plt.show()
