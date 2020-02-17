"""
the program is used to generate the data in need to tune the parameters of motif indicator
"""
import pandas as pd

if __name__ == '__main__':
    base_in = './output/motif/motif_'
    match_in = './data/matches.csv'
    base_out = './output/grade/'

    matches = pd.read_csv(match_in, index_col=0)
    res = pd.DataFrame(columns=['outcome'])
    for i in range(1, 39):
        if matches.loc[i, 'Outcome'] == 'win':
            res.loc[i, 'outcome'] = 1
        else:
            if matches.loc[i, 'Outcome'] == 'loss':
                res.loc[i, 'outcome'] = -1
            else:
                res.loc[i, 'outcome'] = 0
    # res.to_csv(base_out + 'trainY.csv')

    col = []
    for i in range(1, 16):
        col.append('motif_' + str(i))
    ret = pd.DataFrame(columns=col)
    for ID in range(1, 39):
        mo1 = pd.read_csv(base_in + str(ID) + '_1H.csv', header=0, index_col=0)
        mo2 = pd.read_csv(base_in + str(ID) + '_2H.csv', header=0, index_col=0)
        mo = pd.concat([mo1, mo2], axis=0).loc[:, ]
        husk_idx = (mo['team'] == "Huskies")
        oppo_idx = ~husk_idx
        count_motif = pd.DataFrame(columns=col)
        for i in range(1, 16):
            pre_m = 'motif_' + str(i)
            mo_idx = (mo[pre_m] > 0)
            count_motif.loc['Huskies', pre_m] = sum(mo_idx & husk_idx)
            count_motif.loc['Opponent', pre_m] = sum(mo_idx & oppo_idx)
        for i in range(1, 16):
            pre_m = 'motif_' + str(i)
            # ret.loc[ID, pre_m] = count_motif.loc['Huskies', pre_m] / sum(count_motif.loc['Huskies']) - count_motif.loc[
            #     'Opponent', pre_m] / sum(count_motif.loc['Opponent'])
            ret.loc[ID, pre_m] = (count_motif.loc['Huskies', pre_m] - count_motif.loc[
                'Opponent', pre_m]) / (sum(count_motif.loc['Opponent']) + sum(count_motif.loc['Huskies']))
    # ret.to_csv(base_out + 'trainX.csv')
    ret.to_csv(base_out + 'trainX1.csv')
