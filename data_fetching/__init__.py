# data_fetching/__init__.py

# Tuo automaattisesti TeamsDataFetcher, kun paketti tuodaan
from .fetch_factory import DataFetchFactory, TeamsDataFetcher

__all__ = ['DataFetchFactory', 'TeamsDataFetcher']