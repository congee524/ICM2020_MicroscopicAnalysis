"""
the program is used to divide sequences in matches,
record some valuable information in fullevents.csv and matches.csv,
and then count the motifs

the sequences are divided according to the possession of the ball
"""

import pandas as pd
from itertools import permutations
import json


def stat_motif(pass_mat):
    motif_mat = [0 for _ in range(16)]
    p_num = len(pass_mat)
    if p_num < 3:
        if p_num >= 2:
            for p in permutations(range(p_num), 2):
                motif_mat[14] += pass_mat.iloc[p[0], p[1]]
                motif_mat[15] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[0]])
            motif_mat[15] /= 2
            # motif_mat[14] -= motif_mat[15]
        return motif_mat

    # count all motifs
    for p in permutations(range(p_num), 3):
        # choose all possible three players i.e. the permutations
        # and then check that whether the sequence meet some formation conditions of the motifs
        motif_mat[1] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[1], p[2]])
        motif_mat[2] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[1]])
        motif_mat[3] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[1]])
        motif_mat[4] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[0]])
        motif_mat[5] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[0]], pass_mat.iloc[p[1], p[2]])
        motif_mat[6] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[0]], pass_mat.iloc[p[1], p[2]],
                            pass_mat.iloc[p[2], p[1]])
        motif_mat[7] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[1]])
        motif_mat[8] += min(pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]],
                            pass_mat.iloc[p[2], p[1]])
        motif_mat[9] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[0]])
        motif_mat[10] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[0]],
                             pass_mat.iloc[p[1], p[0]])
        motif_mat[11] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[2], p[1]], pass_mat.iloc[p[2], p[0]],
                             pass_mat.iloc[p[1], p[0]])
        motif_mat[12] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[0]],
                             pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[1]])
        motif_mat[13] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[2]], pass_mat.iloc[p[2], p[0]],
                             pass_mat.iloc[p[1], p[0]], pass_mat.iloc[p[2], p[1]], pass_mat.iloc[p[0], p[2]])

    for p in permutations(range(p_num), 2):
        motif_mat[14] += pass_mat.iloc[p[0], p[1]]
        motif_mat[15] += min(pass_mat.iloc[p[0], p[1]], pass_mat.iloc[p[1], p[0]])

    # remove the repeated motif due of the symmetry
    motif_mat[1] /= 2
    motif_mat[4] /= 2
    motif_mat[6] /= 2
    motif_mat[8] /= 2
    motif_mat[9] /= 3
    motif_mat[11] /= 2
    motif_mat[13] /= 3
    motif_mat[15] /= 2

    return motif_mat


def div_seq(seq_csv, full_csv, pd_name, matchID, matchPeriod):
    assert (matchID > 0 & matchID <= 38)
    scene_idx = (seq_csv.loc[:, 'MatchID'] == matchID)
    event_idx = (full_csv.loc[:, 'MatchID'] == matchID)
    output_dir = 'output/motif/motif_' + str(matchID)
    if matchPeriod == '1H' or matchPeriod == '2H':
        scene_idx = scene_idx & (seq_csv.loc[:, 'MatchPeriod'] == matchPeriod)
        event_idx = event_idx & (full_csv.loc[:, 'MatchPeriod'] == matchPeriod)
        output_dir += ('_' + matchPeriod)
    output_dir += '.csv'

    scene = seq_csv.loc[scene_idx].loc[:,
            ['TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'EventTime', 'EventOrigin_x', 'EventDestination_x']]
    scene.index = range(sum(scene_idx))
    scene.columns = ['Team', 'Orig', 'Dest', 'Time', 'ox', 'dx']

    event = full_csv.loc[event_idx].loc[:, ['TeamID', 'EventTime', 'EventType']]
    event.index = range(sum(event_idx))
    event.columns = ['Team', 'Time', 'Event']
    duel_idx = (event.loc[:, 'Event'] == 'Duel')
    shot_idx = (event.loc[:, 'Event'] == 'Shot')
    # split into two teams to count
    hask_idx = (event.loc[:, 'Team'] == 'Huskies')
    oppo_idx = ~hask_idx

    data_store = []

    orig = scene.loc[0, 'Orig']
    dest = orig
    team = scene.loc[0, 'Team']
    s_time = scene.loc[0, 'Time']
    ox = scene.loc[0, 'ox']
    dx = scene.loc[0, 'dx']
    player_inv = set()
    player_inv.add(orig)
    Pass_mat = pd.DataFrame()
    Pass_mat[orig] = 0
    Pass_mat.loc[orig] = 0

    for index, row in scene.iterrows():
        if row['Orig'] != dest:
            # means that the last sequence ended
            e_time = row['Time']
            Motif_mat = stat_motif(Pass_mat)
            tmp_dict = {}
            tmp_dict['player_inv'] = player_inv
            tmp_dict['motif'] = Motif_mat
            tmp_dict['s_time'] = s_time
            tmp_dict['e_time'] = e_time
            tmp_dict['team'] = team
            tmp_dict['ox'] = ox
            tmp_dict['dx'] = dx
            time_idx = (event.loc[:, 'Time'] >= s_time) & (event.loc[:, 'Time'] < e_time)
            if team == 'Huskies':
                tmp_dict['duel'] = sum(time_idx & duel_idx & oppo_idx)
                tmp_dict['shot'] = sum(time_idx & shot_idx & hask_idx)
            else:
                tmp_dict['duel'] = sum(time_idx & duel_idx & hask_idx)
                tmp_dict['shot'] = sum(time_idx & shot_idx & oppo_idx)
            data_store.append(tmp_dict)

            orig = row['Orig']
            dest = row['Dest']
            team = row['Team']
            s_time = row['Time']
            ox = row['ox']
            dx = row['dx']
            player_inv = set()
            player_inv.add(orig)
            player_inv.add(dest)
            Pass_mat = pd.DataFrame()
            Pass_mat[orig] = 0
            Pass_mat.loc[orig] = 0
            Pass_mat[dest] = 0
            Pass_mat.loc[dest] = 0
            Pass_mat.loc[orig, dest] += 1
        else:
            dest = row['Dest']
            dx = row['dx']
            if dest not in player_inv:
                Pass_mat[dest] = 0
                Pass_mat.loc[dest] = 0
                player_inv.add(row['Dest'])
            Pass_mat.loc[row['Orig'], dest] += 1

    e_time = 3900.0 # 3900 is the longest possible time for a match
    Motif_mat = stat_motif(Pass_mat)
    tmp_dict = {}
    tmp_dict['player_inv'] = player_inv
    tmp_dict['motif'] = Motif_mat
    tmp_dict['s_time'] = s_time
    tmp_dict['e_time'] = e_time
    tmp_dict['team'] = team
    tmp_dict['ox'] = ox
    tmp_dict['dx'] = dx
    time_idx = (event.loc[:, 'Time'] >= s_time) & (event.loc[:, 'Time'] < e_time)
    tmp_dict['duel'] = sum(time_idx & duel_idx)
    tmp_dict['shot'] = sum(time_idx & shot_idx)
    data_store.append(tmp_dict)

    data_pd = pd.DataFrame(columns=pd_name)
    for idx, li in enumerate(data_store):
        data_pd.loc[idx, 'team'] = li['team']
        data_pd.loc[idx, 's_time'] = li['s_time']
        data_pd.loc[idx, 'e_time'] = li['e_time']
        data_pd.loc[idx, 'ox'] = li['ox']
        data_pd.loc[idx, 'dx'] = li['dx']
        data_pd.loc[idx, 'dis'] = li['dx'] - li['ox']
        data_pd.loc[idx, 'duel'] = li['duel']
        data_pd.loc[idx, 'shot'] = li['shot']
        for ix in range(1, 16):
            data_pd.loc[idx, 'motif_' + str(ix)] = li['motif'][ix]
        if li['team'] == 'Huskies':
            for name in li['player_inv']:
                data_pd.loc[idx, name] = True

    data_pd.to_csv(output_dir)


if __name__ == '__main__':
    passing_dir = './data/passingevents.csv'
    full_dir = './data/fullevents.csv'
    name_dir = './data/players.json'
    Seq_csv = pd.read_csv(passing_dir,
                          usecols=['MatchID', 'TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'MatchPeriod',
                                   'EventTime', 'EventOrigin_x', 'EventDestination_x'])
    Full_csv = pd.read_csv(full_dir, usecols=['MatchID', 'MatchPeriod', 'EventTime', 'EventType'])
    with open(name_dir) as f:
        player_name = json.load(f)
    Pd_name = ['team', 's_time', 'e_time', 'duel', 'shot', 'ox', 'dx', 'dis']
    for i in range(1, 16):
        Pd_name.append('motif_' + str(i))
    Pd_name += player_name

    for ID in range(1, 39):
        div_seq(Seq_csv, Full_csv, Pd_name, ID, '1H')
        div_seq(Seq_csv, Full_csv, Pd_name, ID, '2H')
