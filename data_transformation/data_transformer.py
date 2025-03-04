import pandas as pd
from typing import Dict, Any
from abc import ABC, abstractmethod
import json

# Strategy interface    
class TransformationStrategy(ABC):
    @abstractmethod
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        pass

# Concrete strategies

class FranchiseTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        df = pd.json_normalize(data["data"])
        df.rename(
            columns={"id": "franchise_id", "fullName": "full_name", "teamCommonName" : "team_common_name", "teamPlaceName" : "team_place_name"},
            inplace=True
            )
        return df
    
class TeamsTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any]) -> pd.DataFrame :
        df = pd.json_normalize(data["data"])
        df.rename(
            columns={"id": "team_id", "franchiseId": "franchise_id", "fullName": "full_name", "leagueId": "league_id", "rawTricode": "raw_tricode", "triCode": "tricode"},
            inplace=True
            )
        return df
    
class ScheduleTransformationStrategy(TransformationStrategy):
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
                'winningGoalie.playerId',
                'winningGoalScorer.playerId']
        games = []
        df = pd.DataFrame
        for i in range(len(data["gameWeek"])):
            games += data["gameWeek"][i]["games"]
        df = pd.json_normalize(games)
        filteredDf = removeNotIncludedKeys(df, fields)
        del (df)
        filteredDf.rename(
            columns={"id": "game_id", "gameType": "game_type", "neutralSite": "neutral_site", "startTimeUTC" : "starttime_utc", "gameState" : "game_state",
                     "awayTeam.id" : "away_team_id", "awayTeam.score" : "away_team_score", "homeTeam.id" : "home_team_id",
                     "homeTeam.score": "home_team_score", "winningGoalie.playerId": "winning_goalie_id", "winningGoalScorer.playerId": "winning_goal_scorer_id"},
            inplace=True
            )
        return filteredDf
    
class RosterTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        fields = ["id",
            "headshot",
            "firstName.default",
            "lastName.default",
            "sweaterNumber",
            "positionCode",
            "shootsCatches",
            "heightInCentimeters",
            "weightInKilograms",
            "birthDate",
            "birthCity.default",
            "birthCountry",
            "birthStateProvince"]
        players = data["forwards"]
        players += data["defensemen"]
        players += data["goalies"]
        df = pd.json_normalize(players)
        filteredDf = removeNotIncludedKeys(df, fields)
        filteredDf['current_team_id'] = kwargs["current_team_id"]
        filteredDf.rename(
            columns={"id":"player_id", "firstName.default":"first_name", "lastName.default":"last_name", "sweaterNumber":"sweater_number", 
            "positionCode": "position_code", "shootsCatches": "shoots_catches", "heightInCentimeters": "height_in_cm", "weightInKilograms": "weight_in_kg", 
            "birthDate": "birth_date", "birthCity.default": "birth_city", "birthCountry": "birth_country", "birthStateProvince": "birth_state_province",
            "headshot": "headshot_url"},
            inplace=True
        )
        return filteredDf


def removeNotIncludedKeys(df: pd.DataFrame, columnList: list) -> pd.DataFrame:
    if columnList == None:
        return df
    for column in df.columns:
        if column not in columnList:
            df = df.drop(column, axis=1)
    return df 


# Context class
class DataTransformer:
    def __init__(self, strategy: TransformationStrategy = None):
        self._strategy = strategy
        
    def set_strategy(self, strategy: TransformationStrategy):
        self._strategy = strategy

    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        return self._strategy.transform(data, **kwargs)