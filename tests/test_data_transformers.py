import unittest
import pipeline as pl

class TestTransformationStrategies(unittest.TestCase):
    
    def test_franchise_transformation(self):
        # Test Franchise data transformation
        data = {
            "data": [
                {
                    "id": 1,
                    "fullName": "Test Franchise",
                    "teamCommonName": "Test Team",
                    "teamPlaceName": "Test Place"
                }
            ]
        }
        strategy = pl.FranchiseTransformationStrategy()
        df = strategy.transform(data)

        self.assertEqual(df.columns.tolist(), 
                         ['franchise_id', 'full_name', 'team_common_name', 'team_place_name'])
        self.assertEqual(df.iloc[0]['franchise_id'], 1)

    def test_teams_transformation(self):
        # Test Teams data transformation
        data = {
            "data": [
                {
                    "id": 1,
                    "franchiseId": 100,
                    "fullName": "Test Team",
                    "leagueId": 2,
                    "rawTricode": "TEST",
                    "triCode": "TST"
                }
            ]
        }
        strategy = pl.TeamsTransformationStrategy()
        df = strategy.transform(data)

        self.assertEqual(df.columns.tolist(), 
                         ['team_id', 'franchise_id', 'full_name', 'league_id', 'raw_tricode', 'tricode'])
        self.assertEqual(df.iloc[0]['team_id'], 1)