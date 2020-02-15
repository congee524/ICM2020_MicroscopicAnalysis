import pandas as pd
from itertools import permutations
import json


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