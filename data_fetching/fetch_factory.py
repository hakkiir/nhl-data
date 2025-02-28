# fetch_factory.py

import requests
from exceptions import APIError
from typing import Self, Dict, Any

endpoints = {
    "dev": 
        {
            "franchise" : "http://localhost:8080/api/franchise.json",
        },
    "prd":
        {
            "franchise" : "https://api.nhle.com/stats/rest/en/franchise",
        }
    }

class DataFetchFactory:
    @staticmethod
    def get_fetcher(data_type: str, env: str) -> Self:
        if data_type == 'teams':
            return TeamsDataFetcher(env)

        else:
            raise ValueError(f"Unknown data type: {data_type}")


class TeamsDataFetcher():
    def __init__(self, env: str):
        self.endpoint = endpoints[env]["franchise"]

    def fetch(self) -> Dict[str, Any]:
        response = requests.get(self.endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIError(f"Error: {response.status_code}, {response.text}")
        