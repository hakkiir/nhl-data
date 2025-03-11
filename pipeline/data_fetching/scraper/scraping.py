import pandas as pd
from typing import Dict

def Scrape_team_to_division_mapping() -> Dict:
    '''
    returns {team: division_id} dictionary 

    '''
    url = "https://en.wikipedia.org/wiki/National_Hockey_League#List_of_teams"
    tables = pd.read_html(url)

    df = tables[2][['Division', 'Team']]

    return df
'''
    mapping = {
        'Central': 1,
        'Pacific': 2,
        'Metropolitan': 3,
        'Atlantic': 4
    }
    df['division_id'] = df['Division'].map(mapping).fillna(0).astype(int)

    output = {}
    for i in range(df.__len__()):
        team = df.loc[i]
        output[team['Team']] = team['division_id']
    return output
'''