import abc
from typing import Dict, Any
import requests
import logging
from exceptions import APIError
from os import getenv
from .endpoints import endpoints

logger = logging.getLogger(__name__)
env = getenv("PLATFORM")

# Abstract base class
class DataFetcher(abc.ABC):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
    
    def fetch(self) -> Dict[str, Any]:
        try:
            response = requests.get(self.endpoint, timeout=10)
            response.raise_for_status()  # HTTPError for bad responses
            logger.info(f"Successfully fetched data from {self.endpoint}")
            print(f"Successfully fetched data from {self.endpoint}")
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"Error fetching {self.endpoint}: {e}")
            raise APIError(f"API request failed: {e}") from e

class FranchiseDataFetcher(DataFetcher):
    def __init__(self):
        super().__init__(endpoints[env]["franchise"])

class TeamsDataFetcher(DataFetcher):
    def __init__(self):
        super().__init__(endpoints[env]["teams"])

class RosterDataFetcher(DataFetcher):
    def __init__(self, team_tricode: str):
        endpoint = endpoints[env]["roster"].replace("<team_tricode>", team_tricode)
        super().__init__(endpoint)

