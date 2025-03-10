import pandas as pd
from typing import Dict
from numpy import select

def Scrape_team_to_division_mapping() -> Dict:
    '''
    returns {team: division_id} dictionary 

    '''
    url = "https://en.wikipedia.org/wiki/National_Hockey_League#List_of_teams"
    tables = pd.read_html(url)

    df = tables[2][['Division', 'Team']]
    df['Team'] = df['Team'].replace('Montreal Canadiens', 'Montréal Canadiens')
    #Montréal Canadiens
    # map divisions to division_id
    '''conditions = [
        (df['Division'] == 'Central'),
        (df['Division'] == 'Pacific'),
        (df['Division'] == 'Metropolitan'),
        (df['Division'] == 'Atlantic')]
    choices = [1, 2, 3, 4]
    df['division_id'] = select(conditions, choices)
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