import pybaseball as pb
import Clustering.cluster as cl
import pickle


def get_pitcher(pitcher):
    return pb.statcast_pitcher('2021-04-01', '2021-10-03', pitcher)


def find_events(cl_num, group, threshold):
    pitchers = cl.get_group_ids(cl_num, group)
    events = []
    for pitcher in pitchers:
        data = get_pitcher(pitcher)
        for _, entry in data[abs(data['delta_home_win_exp']) > threshold].iterrows():
            if entry['inning_topbot'] == 'Bot' and entry['delta_home_win_exp'] > threshold:
                events.append(entry)
            elif entry['inning_topbot'] == 'Top' and entry['delta_home_win_exp'] < -threshold:
                events.append(entry)
    return events


def events_per_gp(cl_num, threshold):
    per_gp = {}
    for i in range(1, cl_num+1):
        per_gp[i] = find_events(cl_num, i, threshold)
    return per_gp


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
