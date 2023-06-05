"""This module contains the functions needed to find significant events for each 
cluster of pitchers identified as the outcome of clustering. A significant event 
is a pitch that resulted in a swing of expected win percentage against a 
pitchers team whose absolute value is greater than the threshold value.

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
import pybaseball as pb
import Clustering.cluster as cl
import pickle

#The threshold win probability swing amount to be considered significant
THRESHOLD = .1


def get_pitcher(pitcher):
    """ Retrieves all pitches thrown in the 2021 season by the specified pitcher

    Arguments: pitcher - the playerID of the pitcher to retrieve data for
    """
    return pb.statcast_pitcher('2021-04-01', '2021-10-03', pitcher)


def find_events(cl_num, group):
    """ Iterates over the pitchers of a certain group identified in clustering, 
    finding all those occurrences which qualify as significant events.

    Arguments: cl_num - the number of clusters in the clustering to load 
               group - the group from the cluster to find events for 
    """
    pitchers = cl.get_group_ids(cl_num, group)
    events = []
    for pitcher in pitchers:
        data = get_pitcher(pitcher)
        for _, entry in data[abs(data['delta_home_win_exp']) > THRESHOLD].iterrows():
            if entry['inning_topbot'] == 'Bot' and entry['delta_home_win_exp'] > threshold:
                events.append(entry)
            elif entry['inning_topbot'] == 'Top' and entry['delta_home_win_exp'] < -threshold:
                events.append(entry)
    return events


def events_per_gp(cl_num):
    """ For every group in the specified clustering, find significant events, 
    and return a dictionary mapping group numbers to lists of significant event
    dataframes.

    Arguments: cl_num - the number of clusters in the clustering to load
    """
    per_gp = {}
    for i in range(cl_num):
        per_gp[i] = find_events(cl_num, i, THRESHOLD)
    with open('gp_events.pickle', 'wb') as pick:
        pickle.dump(per_gp, pick)
    return per_gp
