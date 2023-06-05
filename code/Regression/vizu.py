"""This module contains the functions needed to vizualize fatigue markers in 
time series data accumulated for each group in the pitcher clustering, in order
to provide data viz for the regression analysis. 

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
import matplotlib.pyplot as plt


def plot_game_series(series):
    """Plots the passed in series on a matplotlib graph
    
    Arguments: series - a dataframe containing the data to be plotted
    """
    plt.plot(range(series.shape[0]), series)
    plt.show()