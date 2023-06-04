import pybaseball as pb
import cluster as cl


def find_events(cl_num, group, threshold):
    pitchers = cl.get_group_ids(cl_num, group)
    events = []
    for pitcher in pitchers:
        data = pb.statcast_pitcher('2021-04-01', '2021-10-03', pitcher)
        for entry in data[abs(data['delta_home_win_exp']) > threshold]:
            if entry['inning_topbot'] == 'Bot' and entry['delta_home_win_exp'] > threshold:
                events.append(entry)
            elif entry['inning_topbot'] == 'Top' and entry['delta_home_win_exp'] < -threshold:
                events.append(entry)
    for event in events:
        print(f"{event['game_date']}, {event['player_name']}")

find_events(8, 1, .1)
