import os
import sqlalchemy as db
import argparse
import logging
from data_fetching import * 
from data_transformation import *
from data_persistence import *
import time
import datetime
from exceptions import *

parser = argparse.ArgumentParser()
parser.add_argument('--static', '-s', help="run pipelines for static data", type= bool, default= False)
logger = logging.getLogger(__name__)


def schedule_backfiller(data_fetcher: DataFetchFactory, data_transformer: DataTransformer, dbManager: DatabaseManager, env: str):
    schedule_backfill_generator = data_fetcher.get_fetcher('schedule', env).backfill_generator()
    # backfill 
    data_transformer.set_strategy(ScheduleTransformationStrategy())
    for schedule in schedule_backfill_generator:
        try:
            normalized_schedule = data_transformer.transform(schedule)
        except APIError:
            return
        try:
            dbManager.save_schedule_data(normalized_schedule)
        except SaveToDatabaseError:
            pass

def roster_filler(data_fetcher: DataFetchFactory, data_transformer: DataTransformer, dbManager: DatabaseManager, env: str):
    teams = dbManager.get_teams_in_season()
    for team in teams:
        tricode = team[1]
        team_id = team[0]
        print("team_id:")
        print(team_id)
        print("tricode:")
        print(tricode)
        try:
            roster_data = data_fetcher.get_fetcher('roster', env, team_tricode=tricode).fetch()
            time.sleep(2)
        except KeyError:
            print("exception")
        data_transformer.set_strategy(RosterTransformationStrategy())
        try:
            normalized_roster = data_transformer.transform(roster_data, current_team_id=team_id)
        except Exception as e:
            print(f"exception: {e}")
        try:
            dbManager.save_roster_data(normalized_roster)
        except SaveToDatabaseError as e:
            print(e)
    #    print(team)
    #return 0
    

def main() -> int:
    #logging 
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info(f'Started: {datetime.datetime.now()}')
    args = parser.parse_args()
    
    # db url from env and db connection
    dbUrl = os.getenv('DB_URL')
    engine = db.create_engine(dbUrl)

    #env
    env = os.getenv("PLATFORM")

    # Data Fetching
    data_fetcher    = DataFetchFactory()
    franchise_data  = data_fetcher.get_fetcher('franchise', env).fetch()
    teams_data      = data_fetcher.get_fetcher('teams', env).fetch()
    
    
    # Data Transformation
    data_transformer = DataTransformer()

    data_transformer.set_strategy(FranchiseTransformationStrategy())
    normalized_franchise = data_transformer.transform(franchise_data)

    data_transformer.set_strategy(TeamsTransformationStrategy())
    normalized_teams = data_transformer.transform(teams_data)


    # Data Persistence
    dbManager = DatabaseManager(engine)
    dbManager.save_franchise_data(normalized_franchise)
    dbManager.save_teams_data(normalized_teams)
    schedule_backfiller(data_fetcher, data_transformer, dbManager, env)
    
    roster_filler(data_fetcher, data_transformer, dbManager, env)

if __name__ == '__main__':
    main()