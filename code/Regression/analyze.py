from Regression.finder import *

PITCH_TS = ['FF', 'CU', 'CH', 'SI', 'SL', 'FC', 'FS', 'ST', 'SV']

def get_event(event):
    pitcher = get_pitcher(event['pitcher'])
    game = pitcher[pitcher['game_date'] == event['game_date']]
    return game


def game_stat_series(game, pitchTs, stat):
    return game[game['pitch_type'].isin(pitchTs)].loc[:, stat]


def fb_velo(event):
    return game_stat_series(get_event(event), ['FF'], 'release_speed')

def cv_spin(event):
    return game_stat_series(get_event(event), ['CU'], 'release_spin_rate')
