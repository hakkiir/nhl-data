import pandas as pd
from typing import Dict, Any
from abc import ABC, abstractmethod
from pipeline.data_fetching import scraping

# Strategy interface    
class TransformationStrategy(ABC):
    @abstractmethod
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        pass

# Concrete strategies

class StandingsTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        fields = [
        'division_id',
        'team_id',
        'standing_id', 
        'date',
        'conferenceSequence',
        'divisionSequence',
        'gamesPlayed',
        'goalDifferential',
        'goalAgainst',
        'goalFor',
        'pointPctg',
        'winPctg',
        'homeGamesPlayed',
        'homeGoalDifferential',
        'homeGoalsAgainst',
        'homeGoalsFor',
        'homeLosses',
        'homeOtLosses',
        'homePoints',
        'homeWins',
        'homeRegulationWins',
        'roadGamesPlayed',
        'roadGoalDifferential',
        'roadGoalsAgainst',
        'roadGoalsFor',
        'roadLosses',
        'roadOtLosses',
        'roadPoints',
        'roadWins',
        'roadRegulationWins',
        'streakCode',
        'streakCount',
        'wildcardSequence',
        'wins',
        'losses',
        'points',
        'otLosses',
        'l10Losses',
        'l10Wins',
        'l10OtLosses'
        ]

        databaseManager = kwargs["databasemanager"]
        timeStamp = data["standingsDateTimeUtc"]
        df = pd.json_normalize(data["standings"])

        teams = databaseManager.get_teams_in_season()
        team_mapping = {team[1]: (team[0], team[2]) for team in teams}

        # Apply mapping for division_id and team_id
        df["division_id"] = df["teamAbbrev.default"].map(lambda abb: team_mapping.get(abb, (None, None))[1])
        df["team_id"] = df["teamAbbrev.default"].map(lambda abb: team_mapping.get(abb, (None, None))[0])

        print("standing_id:")
        print(df["divisionAbbrev"]+df["divisionSequence"].astype(str))
        df["standing_id"] = (df["divisionAbbrev"]+df["divisionSequence"].astype(str)).values
        df["date"] = timeStamp
        print(df)
        filteredDf = removeNotIncludedKeys(df, fields)
        filteredDf.rename(
            columns={"date"                 : "standings_datetime", 
                     "conferenceSequence"   : "conference_seq",
                     "divisionSequence"     : "division_seq",
                     "gamesPlayed"          : "games_played",
                     "goalDifferential"     : "goal_diff",
                     "goalAgainst"          : "goals_against",
                     "goalFor"              : "goals_for",
                     "pointPctg"            : "points_pctg",
                     "winPctg"              : "win_pctg",
                     "homeGamesPlayed"      : "home_games_played",
                     "homeGoalDifferential" : "home_goals_diff",
                     "homeGoalsAgainst"     : "home_goals_against",
                     "homeGoalsFor"         : "home_goals_for",
                     "homeLosses"           : "home_losses",
                     "homeOtLosses"         : "home_ot_losses",
                     "homePoints"           : "home_points",
                     "homeWins"             : "home_total_wins",
                     "homeRegulationWins"   : "home_reg_wins",
                     "roadGamesPlayed"      : "road_games_played",
                     "roadGoalDifferential" : "road_goals_diff",
                     "roadGoalsAgainst"     : "road_goals_against",
                     "roadGoalsFor"         : "road_goals_for",
                     "roadLosses"           : "road_losses",
                     "roadOtLosses"         : "road_ot_losses",
                     "roadPoints"           : "road_points",
                     "roadWins"             : "road_total_wins",
                     "roadRegulationWins"   : "road_reg_wins",
                     "streakCode"           : "streak_code",
                     "streakCount"          : "streak_count",
                     "wildcardSequence"     : "wildcard_seq",
                     "otLosses"             : "ot_losses",
                     "l10Losses"            : "l10_losses",
                     "l10Wins"              : "l10_wins" ,
                     "l10OtLosses"          : "l10_ot_losses"
                     },inplace=True) 
        print(filteredDf.head)
        return filteredDf

class FranchiseTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
        df = pd.json_normalize(data["data"])
        df.rename(
            columns={"id": "franchise_id", "fullName": "franchise_name", "teamCommonName" : "team_common_name", "teamPlaceName" : "team_place_name"},
            inplace=True
            )
        return df
    
class TeamsTransformationStrategy(TransformationStrategy):  
    # do something with the result..
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :

        # get divisions ids
        divisions = scraping.Scrape_team_to_division_mapping()
        divisions.rename(columns={"Team": "team_name"}, inplace=True)
        divisions['team_name'] = divisions['team_name'].replace('Montreal Canadiens', 'Montréal Canadiens')
        mapping = {
            'Central': 1,
            'Pacific': 2,
            'Metropolitan': 3,
            'Atlantic': 4
            }     
        divisions['division_id'] = divisions['Division'].map(mapping).fillna(0).astype(int) 

        df = pd.json_normalize(data["data"])
        df.rename(
            columns={"id": "team_id", "franchiseId": "franchise_id", "fullName": "team_name", "leagueId": "league_id", "rawTricode": "raw_tricode", "triCode": "tricode"},
            inplace=True
            )
        
        df_merged = df.merge(divisions[['team_name', 'division_id']], on='team_name', how='left')
    
        return df_merged
    
class ScheduleTransformationStrategy(TransformationStrategy):
    def transform(self, data: Dict[str, Any], **kwargs) -> pd.DataFrame :
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
    if columnList is None or len(columnList) == 0:
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