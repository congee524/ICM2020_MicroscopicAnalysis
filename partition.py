import pandas as pd
from itertools import permutations


def stat_motif(pass_mat):
    motif_mat = [0 for _ in range(14)]
    p_num = len(pass_mat)
    if p_num < 3:
        return motif_mat

    # count all motifs
    for p in permutations(range(p_num), 3):
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

    # remove repeated motifs
    for i in range(1, 13):
        motif_mat[i] -= motif_mat[13]
    for i in range(1, 12):
        motif_mat[i] -= motif_mat[12]
    for i in [2, 4]:
        motif_mat[i] -= motif_mat[11]
    for i in [1, 4, 5, 9]:
        motif_mat[i] -= motif_mat[10]
    for i in []:
        motif_mat[i] -= motif_mat[9]
    for i in [1, 2, 3, 7]:
        motif_mat[i] -= motif_mat[8]
    for i in []:
        motif_mat[i] -= motif_mat[7]
    for i in [1, 2, 3, 4, 5]:
        motif_mat[i] -= motif_mat[6]
    for i in [1, 4]:
        motif_mat[i] -= motif_mat[5]
    for i in []:
        motif_mat[i] -= motif_mat[4]
    for i in [1, 2]:
        motif_mat[i] -= motif_mat[3]

    return motif_mat


def div_seq(seq_csv, matchID, matchPeriod):
    assert (matchID > 0 & matchID <= 38)
    scene_idx = (seq_csv.loc[:, 'MatchID'] == matchID)
    output_dir = 'output/motif_' + str(matchID)
    if matchPeriod == '1H' or matchPeriod == '2H':
        scene_idx = scene_idx & (seq_csv.loc[:, 'MatchPeriod'] == matchPeriod)
        output_dir += ('_' + matchPeriod)
    output_dir += '.csv'

    scene = seq_csv.loc[scene_idx].loc[:,
            ['TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'EventTime', 'EventOrigin_x', 'EventDestination_x']]
    scene.index = range(sum(scene_idx))
    scene.columns = ['Team', 'Orig', 'Dest', 'Time', 'ox', 'dx']

    data_store = []

    orig = scene.loc[0, 'Orig']
    dest = orig
    team = scene.loc[0, 'Team']
    s_time = scene.loc[0, 'Time']
    e_time = s_time
    ox = scene.loc[0, 'ox']
    dx = scene.loc[0, 'dx']
    player_inv = set()
    player_inv.add(orig)
    Pass_mat = pd.DataFrame()
    Pass_mat[orig] = 0
    Pass_mat.loc[orig] = 0

    for index, row in scene.iterrows():
        if row['Orig'] != dest:
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
            data_store.append(tmp_dict)

            orig = row['Orig']
            dest = row['Dest']
            team = row['Team']
            s_time = row['Time']
            e_time = s_time
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
            dx = scene.loc[0, 'dx']
            if dest not in player_inv:
                Pass_mat[dest] = 0
                Pass_mat.loc[dest] = 0
                player_inv.add(row['Dest'])
            Pass_mat.loc[row['Orig'], dest] += 1

    e_time = 3900.0
    Motif_mat = stat_motif(Pass_mat)
    tmp_dict = {}
    tmp_dict['player_inv'] = player_inv
    tmp_dict['motif'] = Motif_mat
    tmp_dict['s_time'] = s_time
    tmp_dict['e_time'] = e_time
    tmp_dict['team'] = team
    tmp_dict['ox'] = ox
    tmp_dict['dx'] = dx
    data_store.append(tmp_dict)

    data_pd = pd.DataFrame()
    for idx, li in enumerate(data_store):
        data_pd.loc[idx, 'team'] = li['team']
        data_pd.loc[idx, 's_time'] = li['s_time']
        data_pd.loc[idx, 'e_time'] = li['e_time']
        data_pd.loc[idx, 'ox'] = li['ox']
        data_pd.loc[idx, 'dx'] = li['dx']
        data_pd.loc[idx, 'dis'] = li['dx'] - li['ox']
        for ix in range(1, 14):
            data_pd.loc[idx, 'motif_' + str(ix)] = li['motif'][ix]
        for name in li['player_inv']:
            data_pd.loc[idx, name] = True

    data_pd.to_csv(output_dir)


if __name__ == '__main__':
    input_dir = './data/passingevents.csv'

    Seq_csv = pd.read_csv(input_dir,
                          usecols=['MatchID', 'TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'MatchPeriod',
                                   'EventTime', 'EventOrigin_x', 'EventDestination_x'])
    # seq_csv.shape = (23429, 6)
    for ID in range(1, 39):
        div_seq(Seq_csv, ID, '1H')
        div_seq(Seq_csv, ID, '2H')
