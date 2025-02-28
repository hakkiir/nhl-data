import pipeline as pl
import os
import sqlalchemy as db
import argparse
import endpoint_urls as urls

import data_fetching as df
from data_transformation import DataTransformer, TeamsTransformationStrategy, FranchiseTransformationStrategy
from data_persistence import DatabaseManager
import time



def main() -> int:
    # db url from env and db connection
    dbUrl = os.getenv('DB_URL')
    engine = db.create_engine(dbUrl)

    #env
    env = os.getenv("PLATFORM")

    # Data Fetching
    data_fetcher    = df.DataFetchFactory()
    schedule_backfill_generator = data_fetcher.get_fetcher('schedule', env).backfill_generator()
    for x in schedule_backfill_generator:
        print(x)
        print()
        print()
        print("=====================================")
        time.sleep(10)
    return 0

main()