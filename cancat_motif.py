import pandas as pd

if __name__ == '__main__':
    base_in = './output/motif/motif_'
    match_in = './data/matches.csv'
    base_out = './output/analysis/Match_'
    eval_dir = './output/analysis/score_motif.csv'
    eval = pd.read_csv(eval_dir, header=0, index_col=0)
    matches = pd.read_csv(match_in, index_col=0)
    col = []
    for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]:
        col.append('motif_' + str(i))
    ret = pd.DataFrame(columns=col + ['coach', 'side', 'scores', 'final_scores', 'outcome'])
    for ID in range(1, 39):
        mo1 = pd.read_csv(base_in + str(ID) + '_1H.csv', header=0, index_col=0)
        mo2 = pd.read_csv(base_in + str(ID) + '_2H.csv', header=0, index_col=0)
        mo = pd.concat([mo1, mo2], axis=0).loc[:, ]
        husk_idx = (mo['team'] == "Huskies")
        oppo_idx = ~husk_idx
        count_motif = pd.DataFrame(columns=col)
        for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]:
            pre_m = 'motif_' + str(i)
            mo_idx = (mo[pre_m] > 0)
            count_motif.loc['Huskies', pre_m] = sum(mo_idx & husk_idx)
            count_motif.loc['Opponent', pre_m] = sum(mo_idx & oppo_idx)
        ans = pd.DataFrame(columns=col + ['coach', 'side', 'scores', 'final_scores', 'outcome'])
        ans.loc['Huskies', 'scores'] = 0
        ans.loc['Opponent', 'scores'] = 0
        for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15]:
            pre_m = 'motif_' + str(i)
            ans.loc['Huskies', pre_m] = count_motif.loc['Huskies', pre_m] / sum(count_motif.loc['Huskies'])
            ans.loc['Opponent', pre_m] = count_motif.loc['Opponent', pre_m] / sum(count_motif.loc['Opponent'])
            ans.loc['Huskies', 'scores'] += (ans.loc['Huskies', pre_m] * eval.loc[pre_m, 'score'])
            ans.loc['Opponent', 'scores'] += (ans.loc['Opponent', pre_m] * eval.loc[pre_m, 'score'])
        ans.loc['Huskies', 'final_scores'] = ans.loc['Huskies', 'scores'] * sum(count_motif.loc['Huskies'])
        ans.loc['Opponent', 'final_scores'] = ans.loc['Opponent', 'scores'] * sum(count_motif.loc['Opponent'])
        ans.loc['Huskies', 'coach'] = matches.loc[ID, 'CoachID']
        ans.loc['Huskies', 'side'] = matches.loc[ID, 'Side']
        ans.loc['Huskies', 'outcome'] = matches.loc[ID, 'Outcome']
        ret = pd.concat([ret, ans], axis=0)
        ans.to_csv(base_out + str(ID) + '.csv')
    ret.to_csv(base_out + 'sum.csv')
