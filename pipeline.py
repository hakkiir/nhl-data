import pandas as pd
import requests
import json
import sqlalchemy as db

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
    def __init__(self, data_path: str, engine: db.Engine):
        self.data_path = data_path
        self.data = None
        self._engine = engine

    def load_data(self, included_fields: list):
        pass

    def run_pipeline(self):
        self.load_data()


class Schedule(DataPipeline):
    def load_data(self):
        response = requests.get(self.data_path)
        if response.status_code == 200:
            self.data = response.json()
            games = self.data["gameWeek"][0]["games"]
            filteredGames = removeNotIncludedKeys(games, CONST_INCLUDED_FIELDS)
            print(filteredGames)
            df = pd.json_normalize(filteredGames)
            print(df.columns)
            print(df)

        else:
            print(f"Error: {response.status_code}")

class Franchise(DataPipeline):
    def __init__(self, data_path: str, engine: db.Engine):
        super().__init__(data_path, engine)

    def load_data(self):

        response = requests.get(self.data_path)

        if response.status_code == 200:
            self.data = response.json()          
            # normalize json data and assign to pandas data frame
            df = pd.json_normalize(self.data["data"])
            # rename columns to match db schema 
            df.rename(
                columns={"id": "id", "fullName": "name", "teamCommonName": "common_name", "teamPlaceName": "place_name"},
                inplace=True
                )
            # insert into db
            df.to_sql("franchise", self._engine, if_exists='replace', index=False)

        else:
            print(f"Error: {response.status_code}")

def removeNotIncludedKeys(lst: list, keyIter: list) -> list:
    if keyIter == None:
        return lst
    output = []
    for item in lst:
        output.append({
        k:v
        for k,v in item.items() if k in keyIter
    })
    return output