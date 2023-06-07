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
from Regression.analyze import *
import pickle
import Regression.vizu as v
from pybaseball import cache

#Stats to collect deltas for per the listed pitches
DELTAS = [(['FF', 'SI', 'FC'], 'release_speed'), (['CU', 'SL'], 'release_speed'), (['CH'], 'release_speed'),
          (['FF', 'SI', 'FC'], 'release_spin_rate'), (['CU', 'SL'], 'release_spin_rate'), (['CH'], 'release_spin_rate'),
          (["FF", "SI", 'FC', 'CU', 'SL', 'CH'], 'release_pos_z'), (["SL"], 'pfx_x'), (["CU"], 'pfx_z')]



def get_all_deltas(group_num):
    """For all the fatigue events found for all the groups in a group_num 
    clustering, computes the deltas of the statistics per those pitches given 
    in the deltas array and stores them in the deltas pickle file
    """
    with open('deltas.pickle', 'rb') as pick:
        gps = pickle.load(pick)
    for group in range(0, 1):
        gp_deltas = {}
        for index, stat in enumerate(DELTAS):
            gp_deltas[index] = avg_group_delta(group, stat[0], stat[1])
        gps.append(gp_deltas)
        with open('deltas.pickle', 'wb') as pick:
            pickle.dump(gps, pick)
    return gps
            
        

#Main executable - Write analysis script here
if __name__ == "__main__":
    #while True:
        #try:
            #cache.enable()
            #cache.purge()
            #get_all_deltas(8)
            #break
        #except KeyError:
            #print("Error - restarting")
            #continue
    deltas = load_deltas()
    for group in deltas:
        print(group)