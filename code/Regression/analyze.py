""" This module contains the functions needed to perform an analysis of the time
series data found leading up to the significant events identified by the finder 
module. 

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
from Regression.finder import *
import math

#Valid Pitch types, for reference
PITCH_TS = ['FF', 'CU', 'CH', 'SI', 'SL', 'FC', 'FS', 'ST', 'SV']

#The name of the pickle file containing the found events for each cluster
DATA_PICKLE = 'gp_events.pickle'

SPIN_DRIFTS = [(-.84, -1.43, -.25), (-1.25, -.019, -.83), (-.71, -.67, -.65), 
               (-1.31, -.97, -.07), (-.32, -1.57, -.89), (-1.83, -.45, -.33),
               (-.56, -.27, -1.34), (-1.19, -.28, -.37)]


def from_pick(group=None):
    """Retrieves the event data found by the finder module for each group in the 
    clustering.

    Arguments: group (opt): a group to retrieve the list of events for. If not 
    specified, returns the dictionary mapping every group to a list of events
    """
    with open(DATA_PICKLE, 'rb') as pick:
        events = pickle.load(pick)
    if group == None:
        return events 
    else:
        return events[group]


def get_event(event):
    """ Gets all the data from a pitcher's performance in a game up to the point 
    in the game at which the significant event occurred.

    Arguements: event - the dataframe of the pitch of the significant event
    """
    date = event['game_date']
    pitcher = get_pitcher(event['pitcher'], start=date, end=date)
    game = pitcher[pitcher['game_date'] == date]
    game = game[game['pitch_number'] <= event['pitch_number']]
    return game


def game_stat_series(game, pitchTs, stat):
    """ Returns a dataframe containing the stat specified for pitches of the 
    types included in the passed pitch type list.

    Arguments: game - the frame containing all series data for the pitcher in
                      the significant game
               pitchTs - A list of pitch types
               stat - the desired stat to get data for over the game 
    """
    return smooth_series(game[game['pitch_type'].isin(pitchTs)].loc[:, stat])


def series_for_group(group_num, pitchTs, stat):
    """Gets all the smoothened time series of the given stat for the given 
    pitches across all events found for a certain clustering group
    
    Arguments: group_num - clustering group number
               pitchTs - an array of pitch types to compute stats for
               stat - the stat to take time series of
    """
    return [game_stat_series(get_event(event), pitchTs, stat) for event in 
            from_pick(group=group_num)]


def series_delta(series):
    """ Computes the change in sliding average across a time series of pitches 
    prior to a fatigue event

    Arguments: series - the smoothened time series to take the delta of
    """
    if series.count() > 0:
        return series.iloc[series.count()-1] - series.iloc[0]
    else:
        return None


def avg_group_delta(group_num, pitchTs, stat):
    """ Takes the average delta of sliding averages of the given stat 
    for the given pitches across all fatigue events identified for the clustering
    group given by group_num

    Arguments: group_num - the clustering group number 
               pitchTs - an array of pitch types to compute the given stat on
               stat - the desired stat to compute the average delta over
    """
    total = 0
    cnt = 0
    for series in series_for_group(group_num, pitchTs, stat):
        delta = series_delta(series)
        if delta != None and not math.isnan(delta):
            cnt += 1
            total += delta
    if cnt == 0:
        return 0
    return total / cnt


def smooth_series(series):
    """Applies an exponential smoothing algorithm to the time series of data 
    which is found for each significant event, based on weighting the immediate
    fatigue effects of pitches thrown within the current inning more than those 
    thrown more than an inning ago.

    Arguments: series - A time series of a metric to smooth the data over
    """
    #Pitches per inning in 2021 = 16.657
    return series.ewm(halflife=8.329).mean()


def load_deltas():
    with open("deltas.pickle", 'rb') as pick:
        return pickle.load(pick)
