import pandas as pd
from typing import Dict, Any


class DataTransformer:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        return self.strategy.transform(data)
    

class FranchiseTransformationStrategy:
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        df = pd.json_normalize(data["data"])
        return df
    
class TeamsTransformationStrategy:
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        df = pd.json_normalize(data["data"])
        return df
    
class ScheduleTransformationStrategy:
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        fields = ['id', 
                'season', 
                'gameType', 
                'neutralSite', 
                'startTimeUTC', 
                'gameState',
                'awayTeam.id', 
                'awayTeam.score',
                'homeTeam.id', 
                'homeTeam.score', 
                'periodDescriptor.number',
                'periodDescriptor.periodType', 
                'periodDescriptor.maxRegulationPeriods',
                'gameOutcome.lastPeriodType', 
                'winningGoalie.playerId',
                'winningGoalScorer.playerId']
        
        games = data["gameWeek"][0]["games"]
        filteredGames = removeNotIncludedKeys(games, fields)
        df = pd.json_normalize(filteredGames)
        return df
    


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