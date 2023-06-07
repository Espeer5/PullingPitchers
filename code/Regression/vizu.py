"""This module contains the functions needed to vizualize fatigue markers in 
time series data accumulated for each group in the pitcher clustering, in order
to provide data viz for the regression analysis. 

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
import matplotlib.pyplot as plt
from Regression.analyze import *


def plot_game_series(series):
    """Plots the passed in series on a matplotlib graph
    
    Arguments: series - a dataframe containing the data to be plotted
    """
    plt.plot(range(series.shape[0]), series)
    plt.show()

def plot_spin_drift():
    gp_colors = ['grey', 'grey', 'grey', 'blue','blue', 'blue', 'orange', 
                 'orange', 'orange', 'red', 'red', 'red', 'green', 'green', 
                 'green', 'yellow', 'yellow', 'yellow', 'brown', 'brown',
                 'brown', 'black', 'black', 'black']
    pitches = []
    for group in SPIN_DRIFTS:
        for spin in group:
            pitches.append(spin)
    labels = ["FB1", "BB1", "CH1", "FB2", "BB2", "CH2", "FB3", "BB3", "CH3", 
              "FB4", "BB4", "CH4", "FB5", "BB5", "CH5", "FB6", "BB6", "CH6",
              "FB7", "BB7", "CH7", "FB8", "BB8", "CH8"]
    plt.bar(labels, height=pitches, color=gp_colors)
    plt.title("Spin Drifts Per Group in Std. Dev's")
    plt.ylabel("Drift Before Fatigue Event (std. dev)")
    plt.xlabel("Pitch Cluster for Group")
    plt.show()