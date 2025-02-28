# data_fetching/__init__.py

# Tuo automaattisesti TeamsDataFetcher, kun paketti tuodaan
from .fetch_factory import DataFetchFactory, FranchiseDataFetcher

__all__ = ['DataFetchFactory', 'FranchiseDataFetcher']