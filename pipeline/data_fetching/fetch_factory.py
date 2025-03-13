from .data_fetchers import (
    DataFetcher, 
    TeamsDataFetcher, 
    FranchiseDataFetcher, 
    RosterDataFetcher,
    StandingsDataFetcher
)
from .schedule_fetcher import ScheduleDataFetcher, ScheduleBackfillFetcher

class DataFetchFactory:
    
    @staticmethod
    def get_fetcher(
        data_type: str
    ) -> DataFetcher:
        """
        Create and return the appropriate data fetcher.
        :param data_type: Type of data to fetch
        :return: Appropriate DataFetcher instance
        :raises ValueError: If an unknown data type is requested
        """
        fetcher_map = {
            'teams': TeamsDataFetcher,
            'franchise': FranchiseDataFetcher,
            'roster': RosterDataFetcher,
            'schedule': ScheduleDataFetcher,
            'schedule_backfill': ScheduleBackfillFetcher,
            'current_standings': StandingsDataFetcher
        }
        
        try:
            return fetcher_map[data_type]()
        except KeyError:
            raise ValueError(f"Unknown data type: {data_type}")