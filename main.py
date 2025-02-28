import pipeline as pl
import os
import sqlalchemy as db
import argparse
import endpoint_urls as urls

import data_fetching as df
from data_transformation import DataTransformer, TeamsTransformationStrategy, FranchiseTransformationStrategy
from data_persistence import DatabaseManager

parser = argparse.ArgumentParser()
parser.add_argument('--static', '-s', help="run pipelines for static data", type= bool, default= False)



def main() -> int:
    args = parser.parse_args()
    
    # db url from env and db connection
    dbUrl = os.getenv('DB_URL')
    engine = db.create_engine(dbUrl)

    #env
    env = os.getenv("PLATFORM")

    # Data Fetching
    data_fetcher    = df.DataFetchFactory()
    franchise_data  = data_fetcher.get_fetcher('franchise', env).fetch()
    teams_data      = data_fetcher.get_fetcher('teams', env).fetch()

    # Data Transformation
    normalized_franchise    = DataTransformer(FranchiseTransformationStrategy()).transform(franchise_data)
    normalized_teams        = DataTransformer(TeamsTransformationStrategy()).transform(teams_data)

    # Data Persistence
    dbManager = DatabaseManager(engine)
    dbManager.save_franchise_data(normalized_franchise)
    dbManager.save_teams_data(normalized_teams)

    
    return 0

if __name__ == '__main__':
    main()