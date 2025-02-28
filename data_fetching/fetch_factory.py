# fetch_factory.py

import requests
from exceptions import APIError
from typing import Self, Dict, Any
from datetime import datetime

endpoints = {
    "dev": 
        {
            "franchise"         : "http://localhost:8080/api/franchise.json",
            "schedule"          : "http://localhost:8080/api/schedule.json",
            "teams"             : "http://localhost:8080/api/teams.json",
        },
    "prd":
        {
            "franchise"         : "https://api.nhle.com/stats/rest/en/franchise",
            "schedule"          : "https://api-web.nhle.com/v1/schedule/now",
            "teams"             : "https://api.nhle.com/stats/rest/en/team"
        }
    }

class DataFetchFactory:
    def __init__(self):
        self.endpoint = None
    @staticmethod
    def get_fetcher(data_type: str, env: str) -> Self:
        if data_type == 'teams':
            return TeamsDataFetcher(env)
        if data_type == 'franchise':
            return FranchiseDataFetcher(env)
        if data_type == 'schedule':
            return ScheduleDataFetcher(env)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
        
    def fetch(self) -> Dict[str, Any]:
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError(f"Error: {response.status_code}, {response.text}")


class FranchiseDataFetcher(DataFetchFactory):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["franchise"]

class TeamsDataFetcher(DataFetchFactory):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["teams"]
        
class ScheduleDataFetcher(DataFetchFactory):
    def __init__(self, env: str):
        super().__init__()
        self.endpoint = endpoints[env]["schedule"]

    def backfill_generator(self):
        self.endpoint = endpoints["prd"]["schedule"]
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            json_data = response.json()
            season_start_date = json_data["regularSeasonStartDate"]
            #season_end_date = json_data["regularSeasonEndDate"]
        else:
            raise APIError(f"Error: {response.status_code}, {response.text}")

        self.endpoint = "https://api-web.nhle.com/v1/schedule/"+season_start_date
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            json_data = response.json()
            nextDate = json_data["nextStartDate"]
        else:
            raise APIError(f"Error: {response.status_code}, {response.text}")
        while toDateTime(nextDate) < datetime(2024, 10, 31):
            yield json_data  
            self.endpoint = "https://api-web.nhle.com/v1/schedule/"+nextDate
            response = requests.get(self.endpoint)
            json_data = response.json()
            nextDate = json_data["nextStartDate"]
        
def toDateTime(json_date: str) -> datetime:
    return datetime.strptime(json_date, "%Y-%m-%d")