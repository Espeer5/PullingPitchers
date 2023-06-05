""" This module contains the functions needed to perform an analysis of the time
series data found leading up to the significant events identified by the finder 
module. 

Author: Edward Speer
Date: 6/5/23
"""

#Module imports
from Regression.finder import *

#Valid Pitch types, for reference
PITCH_TS = ['FF', 'CU', 'CH', 'SI', 'SL', 'FC', 'FS', 'ST', 'SV']

#The name of the pickle file containing the found events for each cluster
DATA_PICKLE = 'gp_events.pickle'


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
    pitcher = get_pitcher(event['pitcher'])
    game = pitcher[pitcher['game_date'] == event['game_date']]
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
    return game[game['pitch_type'].isin(pitchTs)].loc[:, stat]


def smooth_series(series):
    """Applies an exponential smoothing algorithm to the time series of data 
    which is found foor each significant event, based on weighting the immediate
    fatigue effects of pitches thrown within the current inning more than those 
    thrown more than an inning ago.

    Arguments: series - A time series of a metric to smooth the data over
    """
    #Pitches per inning in 2021 = 16.657
    return series.ewm(halflife=8.329).mean()


#Applications of the game_stat_series function for specific stats
def fb_velo(event):
    """Returns the time series of fastball velocity"""
    return game_stat_series(get_event(event), ['FF'], 'release_speed')


def cv_spin(event):
    """Returns the time series of curveball spin"""
    return game_stat_series(get_event(event), ['CU'], 'release_spin_rate')
