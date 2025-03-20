# Tuo automaattisesti TeamsDataFetcher, kun paketti tuodaan
from .database_manager import DatabaseManager, insert_divisions, insert_seasons

__all__ = ['DatabaseManager', 'insert_divisions', 'insert_seasons']