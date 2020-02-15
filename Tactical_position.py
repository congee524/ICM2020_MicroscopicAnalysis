import pandas as pd
import json


def cal_pos(event, player_name):
    data_pd = pd.DataFrame(columns=['pos_x', 'pos_y'])
    for name in player_name:
        orig_idx = (event['OriginPlayerID'] == name)
        dest_idx = (event['DestinationPlayerID'] == name)
        num = sum(orig_idx) + sum(dest_idx)
        if num == 0:
            continue
        pos_x = (sum(event.loc[orig_idx, 'EventOrigin_x']) + sum(event.loc[dest_idx, 'EventDestination_x'])) / num
        pos_y = (sum(event.loc[orig_idx, 'EventOrigin_y']) + sum(event.loc[dest_idx, 'EventDestination_y'])) / num
        data_pd.loc[name, 'pos_x'] = pos_x
        data_pd.loc[name, 'pos_y'] = pos_y
    return data_pd


if __name__ == '__main__':
    full_dir = './data/fullevents.csv'
    name_dir = './data/players.json'
    full_csv = pd.read_csv(full_dir,
                           usecols=['MatchID', 'TeamID', 'OriginPlayerID', 'DestinationPlayerID', 'MatchPeriod',
                                    'EventOrigin_x', 'EventOrigin_y', 'EventDestination_x', 'EventDestination_y'])
    full_csv = full_csv.dropna(axis=0, how='any')
    with open(name_dir) as f:
        Player_name = json.load(f)

    for ID in range(1, 39):
        event_idx = (full_csv.loc[:, 'MatchID'] == ID) & (full_csv.loc[:, 'MatchPeriod'] == '1H')
        Event = full_csv.loc[event_idx].loc[:,
                ['OriginPlayerID', 'DestinationPlayerID', 'EventOrigin_x', 'EventOrigin_y',
                 'EventDestination_x', 'EventDestination_y']]
        data_pd = cal_pos(Event, Player_name)
        output_dir = 'output/pos/pos_' + str(ID) + '_1H.csv'
        data_pd.to_csv(output_dir)

        event_idx = (full_csv.loc[:, 'MatchID'] == ID) & (full_csv.loc[:, 'MatchPeriod'] == '2H')
        Event = full_csv.loc[event_idx].loc[:,
                ['OriginPlayerID', 'DestinationPlayerID', 'EventOrigin_x', 'EventOrigin_y',
                 'EventDestination_x', 'EventDestination_y']]
        data_pd = cal_pos(Event, Player_name)
        output_dir = 'output/pos/pos_' + str(ID) + '_2H.csv'
        data_pd.to_csv(output_dir)
