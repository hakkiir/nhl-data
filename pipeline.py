import pandas as pd
import requests
import json

CONST_EXCLUDED_FIELDS = ["tvBroadcasts", "oddsPartners"]
CONST_INCLUDED_FIELDS = ['id', 
'season', 
'gameType', 
'neutralSite', 
'startTimeUTC', 
'gameState',
'awayTeam', 
'awayTeam.id', 
'awayTeam.commonName.default',
'awayTeam.abbrev', 
'awayTeam.score',
'homeTeam', 
'homeTeam.id', 
'homeTeam.commonName.default',
'homeTeam.abbrev','homeTeam.score', 
'periodDescriptor.number',
'periodDescriptor.periodType', 
'periodDescriptor.maxRegulationPeriods',
'gameOutcome.lastPeriodType', 
'winningGoalie.playerId',
'winningGoalie.firstInitial.default', 
'winningGoalie.lastName.default',
'winningGoalScorer.playerId', 
'winningGoalScorer.firstInitial.default',
'winningGoalScorer.lastName.default']

class DataPipeline:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        #response = requests.get(self.data_path)
        if 1: #response.status_code == 200:
            #data = response.json()
            data = json.load(open("testdata.json"))
            games = data["gameWeek"][0]["games"]
            #for key in games[0]:
            #    print(key)
            filteredGames = removeNotIncludedKeys(games, CONST_INCLUDED_FIELDS)
            print(filteredGames)
            df = pd.json_normalize(filteredGames)
            print(df.columns)
            print(df)
       # else:
            #print(f"Error: {response.status_code}")

            #df = pd.DataFrame(data)
           #print(df)
            ##print(json.dumps(data, indent=2))  # Pretty-print the JSON response
            ##print(data)


    def run_pipeline(self):
        self.load_data()



def removeNotIncludedKeys(lst: list, keyIter: list) -> list:
    output = []
    for item in lst:
        output.append({
        k:v
        for k,v in item.items() if k in keyIter
    })
    return output