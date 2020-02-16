import pandas as pd
import math


if __name__ == '__main__':
    base_dir = './output/motif/motif_'
    col = ['team', 'duel', 'dis']
    for i in range(1, 16):
        col.append('motif_' + str(i))

    output_base_dir = './output/analysis/score_motif.csv'
    mo = pd.DataFrame(columns=col)
    ans = pd.DataFrame(columns=['times', 'dis', 'duel'])
    for ID in range(1, 39):
        mo1 = pd.read_csv(base_dir + str(ID) + '_1H.csv', usecols=col)
        mo2 = pd.read_csv(base_dir + str(ID) + '_2H.csv', usecols=col)
        mo = pd.concat([mo, mo1, mo2], axis=0)
    husk_idx = (mo['team'] == 'Huskies')
    scene = mo.loc[husk_idx]
    for i in range(1, 16):
        pre_m = 'motif_' + str(i)
        mo_idx = (scene[pre_m] > 0)
        ans.loc[pre_m, 'times'] = sum(mo_idx)
        ans.loc[pre_m, 'dis'] = sum(scene.loc[mo_idx, 'dis']) / sum(mo_idx)
        ans.loc[pre_m, 'duel'] = sum(scene.loc[mo_idx, 'duel']) / sum(mo_idx)
        ans.loc[pre_m, 'score'] = ans.loc[pre_m, 'dis'] * ans.loc[pre_m, 'duel']

    ans.to_csv(output_base_dir)