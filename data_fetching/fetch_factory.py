from .data_fetchers import (
    DataFetcher, 
    TeamsDataFetcher, 
    FranchiseDataFetcher, 
    RosterDataFetcher
)
from .schedule_fetcher import ScheduleDataFetcher

class DataFetchFactory:
    
    @staticmethod
    def get_fetcher(
        data_type: str,
        **kwargs
    ) -> DataFetcher:
        """
        Create and return the appropriate data fetcher.
        
        :param data_type: Type of data to fetch
        :param endpoints: Dictionary of endpoints
        :param kwargs: Additional arguments for specific fetchers
        :return: Appropriate DataFetcher instance
        :raises ValueError: If an unknown data type is requested
        """
        fetcher_map = {
            'teams': TeamsDataFetcher,
            'franchise': FranchiseDataFetcher,
            'roster': RosterDataFetcher,
            'schedule': ScheduleDataFetcher
        }
        
        try:
            if data_type == 'roster':
                if 'team_tricode' not in kwargs:
                    raise ValueError("team_tricode is required for roster fetcher")
                return fetcher_map[data_type](kwargs['team_tricode'])
            
            return fetcher_map[data_type]()
        
        except KeyError:
            raise ValueError(f"Unknown data type: {data_type}")