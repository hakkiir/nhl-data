import unittest
from unittest.mock import Mock, patch
import pandas as pd
import requests
from sqlalchemy import create_engine
import pipeline as pl
import datetime 
class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create a test in-memory SQLite database
        self.engine = create_engine('sqlite:///:memory:')

    def test_save_franchise_data(self):
        # Test saving franchise data
        db_manager = pl.DatabaseManager(self.engine)
        df = pd.DataFrame({
            'franchise_id': [1, 2],
            'full_name': ['Team A', 'Team B'],
            'team_common_name': ['teama', 'teamb'],
            'team_place_name': ['Center A', 'Center B']
        })
        
        # Mock the to_sql method
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            db_manager.load(df, 'franchise')
            # Verify to_sql was called with the right parameters
            mock_to_sql.assert_called_once()