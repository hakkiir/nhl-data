import unittest
from unittest.mock import Mock, patch
import requests
import pipeline.data_fetching as pl
from pipeline.exceptions import APIError

class TestDataFetcher(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_success(self, mock_get):
        # Mock a successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        fetcher = pl.DataFetcher("http://test-endpoint.com")
        result = fetcher.fetch()

        self.assertEqual(result, {"test": "data"})
        mock_get.assert_called_once_with("http://test-endpoint.com", timeout=10)

    @patch('requests.get')
    def test_fetch_api_error(self, mock_get):
        # Mock a failed API response
        mock_get.side_effect = requests.RequestException("Connection error")

        fetcher = pl.DataFetcher("http://test-endpoint.com")
        
        with self.assertRaises(APIError):
            fetcher.fetch()
'''
class TestDataFetchFactory(unittest.TestCase):
    def test_get_fetcher(self):
        # Test retrieving different types of fetchers
        franchise_fetcher = pl.DataFetchFactory.get_fetcher('franchise')
        self.assertIsInstance(franchise_fetcher, pl.FranchiseDataFetcher)

        teams_fetcher = pl.DataFetchFactory.get_fetcher('teams')
        self.assertIsInstance(teams_fetcher, pl.TeamsDataFetcher)

        roster_fetcher = pl.DataFetchFactory.get_fetcher('roster')
        self.assertIsInstance(roster_fetcher, pl.RosterDataFetcher)

        schedule_fetcher = pl.DataFetchFactory.get_fetcher('schedule')
        self.assertIsInstance(schedule_fetcher, pl.ScheduleDataFetcher)

    def test_get_fetcher_invalid(self):
        # Test getting an invalid fetcher type
        with self.assertRaises(ValueError):
            pl.DataFetchFactory.get_fetcher('invalid_type')

class TestRosterDataFetcher(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_with_team_tricode(self, mock_get):
        # Mock a successful roster fetch
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"players": []}
        mock_get.return_value = mock_response

        fetcher = pl.RosterDataFetcher()
        result = fetcher.fetch("TOR")

        self.assertEqual(result, {"players": []})

    def test_fetch_empty_tricode(self):
        # Test fetching with an empty team tricode
        fetcher = pl.RosterDataFetcher()
        
        with self.assertRaises(ValueError):
            fetcher.fetch("")


class TestScheduleBackfillFetcher(unittest.TestCase):
    @patch('requests.get')
    def test_backfill_generator(self, mock_get):
        # Mock responses for backfill generator
        mock_responses = [
            Mock(status_code=200, json=lambda: {"nextStartDate": "2024-10-05", "games": []}),
            Mock(status_code=200, json=lambda: {"nextStartDate": "2024-10-06", "games": []}),
        ]
        mock_get.side_effect = mock_responses

        fetcher = pl.ScheduleBackfillFetcher()
        generator = fetcher.backfill_generator(next_date="2024-10-04", end_date="2024-10-07")

        # Collect results from generator
        results = list(generator)

        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(r, dict) for r in results))
'''
if __name__ == '__main__':
    unittest.main()