"""This is the main module used for data analysis on the fatigue of MLB pitchers 
and its indicators in time series across games. The tree is set up such that any 
of the funcitons given in the submodules may be called here for the purposes of 
data analysis.

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
import Clustering.cluster as cl
import Regression.finder as fn
import Regression.analyze as az
import pickle
import Regression.vizu as v


#Main executable - Write analysis script here
if __name__ == "__main__":
    v.plot_game_series(az.smooth_series(az.fb_velo(az.from_pick(group=1)[0])))