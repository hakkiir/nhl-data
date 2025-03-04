# fetch_factory.py
import logging
import requests
from exceptions import APIError
from typing import Self, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod
import json

logger = logging.getLogger(__name__)
endpoints = {
    "dev": 
        {
            "franchise"         : "http://localhost:8080/api/franchise.json",
            "schedule"          : "http://localhost:8080/api/schedule.json",
            "teams"             : "http://localhost:8080/api/teams.json",
            "roster"            : "https://api-web.nhle.com/v1/roster/<team_tricode>/current",
        },
    "prd":
        {
            "franchise"         : "https://api.nhle.com/stats/rest/en/franchise",
            "schedule"          : "https://api-web.nhle.com/v1/schedule/now",
            "teams"             : "https://api.nhle.com/stats/rest/en/team",
            "roster"            : "https://api-web.nhle.com/v1/roster/<team_tricode>/current",
        }
    }

# Abstract product
class DataFetcher(ABC):
    def __init__(self):
        self.endpoint = None
    def fetch(self) -> Dict[str, Any]:
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            logger.info(f"fetched {self.endpoint} succesfully")
            return response.json()
            
        else:
            logger.info(f"error fetching {self.endpoint}")
            raise APIError(f"Error: {response.status_code}, {response.text}")

# Concrete products
class FranchiseDataFetcher(DataFetcher):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["franchise"]

class TeamsDataFetcher(DataFetcher):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["teams"]
        
class ScheduleDataFetcher(DataFetcher):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["schedule"]

    def backfill_generator(self, next_date: str = "2024-10-04", end_date: str ="2025-04-17") -> Any:
        while toDateTime(next_date) < toDateTime(end_date):
            #self.endpoint = "https://api-web.nhle.com/v1/schedule/"+next_date
            self.endpoint = f"http://localhost:8080/api/schedule/{next_date}.json"
            response = requests.get(self.endpoint)
            if response.status_code == 200:
                logger.info(f"fetched {self.endpoint} succesfully")
                json_data = response.json()
                print(f"next date: {next_date}")
                yield json_data
                 # Writing to sample.json
                with open(f"test_server/api/schedule/{next_date}.json", "w+") as outfile:
                    outfile.write(json.dumps(json_data))
                    outfile.close()
                try:
                    next_date = json_data["nextStartDate"]
                except KeyError:
                    return

            else:
                raise APIError(f"Error: {response.status_code}, {response.text}")

class RosterDataFetcher(DataFetcher):
    def __init__(self, env: str, team_tricode: str):
        super().__init__()
        self.endpoint = endpoints[env]["roster"].replace("<team_tricode>", team_tricode)
        #self.endpoint = "http://localhost:8080/api/roster.json"
   

# Factory
class DataFetchFactory:
    @staticmethod
    def get_fetcher(data_type: str, env: str, **kwargs) -> DataFetcher:
        if data_type == 'teams':
            return TeamsDataFetcher(env)
        if data_type == 'franchise':
            return FranchiseDataFetcher(env)
        if data_type == 'schedule':
            return ScheduleDataFetcher(env)
        if data_type == 'roster':
            try:
                return RosterDataFetcher(env, kwargs["team_tricode"])
            except KeyError:
                return KeyError
        else:
            raise ValueError(f"Unknown data type: {data_type}")


def toDateTime(json_date: str) -> datetime:
    return datetime.strptime(json_date, "%Y-%m-%d")