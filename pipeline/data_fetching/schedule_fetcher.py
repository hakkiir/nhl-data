import logging
import requests
from .data_fetchers import DataFetcher
import datetime
from typing import Any
from pipeline.exceptions import APIError
from .endpoints import endpoints
from os import getenv

logger = logging.getLogger(__name__)
env = getenv("PLATFORM")

class ScheduleDataFetcher(DataFetcher):
    def __init__(self):
        super().__init__(endpoints[env]["schedule"])

class ScheduleBackfillFetcher(DataFetcher):
    def __init__(self):
        super().__init__(endpoints[env]["schedule"])
    def backfill_generator(self, next_date: str = "2024-10-04", end_date: str ="2025-04-17") -> Any:

        while datetime.datetime.strptime(next_date, "%Y-%m-%d") < datetime.datetime.strptime(end_date, "%Y-%m-%d"):
            #self.endpoint = "https://api-web.nhle.com/v1/schedule/"+next_date
            self.endpoint = f"http://localhost:8080/api/schedule/{next_date}.json"
            try: 
                response = requests.get(self.endpoint, timeout=10)
                response.raise_for_status()  # HTTPError for bad responses
                if response.status_code == 200:
                    logger.info(f"fetched {self.endpoint} succesfully")
                    json_data = response.json()
                    print(f"next date: {next_date}")
                    yield json_data
                    try:
                        next_date = json_data["nextStartDate"]
                    except KeyError:
                        return
            except requests.RequestException as e:
                logger.error(f"Error fetching {self.endpoint}: {e}")
                raise APIError(f"API request failed: {e}") from e

