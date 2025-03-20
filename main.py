import os
import sqlalchemy as db
#import argparse
import logging
from pipeline import (
    create_nhl_franchise_pipeline,
    create_nhl_roster_pipeline,
    create_nhl_schedule_backfill_pipeline,
    create_nhl_teams_pipeline,
    insert_divisions,
    create_nhl_current_standings_pipeline,
    insert_seasons
)

#parser = argparse.ArgumentParser()
#parser.add_argument('--static', '-s', help="run pipelines for static data", type= bool, default= False)

def main() -> int:

    #logging 
    logging.basicConfig(filename='nhl_workflow.log', level=logging.INFO)
    #logger.info(f'Started: {datetime.datetime.now()}')
    #args = parser.parse_args()
    
    # db url from env and db connection
    dbUrl = os.getenv('DB_URL')
    engine = db.create_engine(dbUrl)

    franchise_wf    = create_nhl_franchise_pipeline(engine)
    teams_wf        = create_nhl_teams_pipeline(engine)
    schedule_wf     = create_nhl_schedule_backfill_pipeline(engine)
    roster_wf       = create_nhl_roster_pipeline(engine)
    standings_wf    = create_nhl_current_standings_pipeline(engine)

    insert_divisions(engine)
    insert_seasons(engine)
    franchise_wf.run()
    teams_wf.run()
    schedule_wf.backfill()
    roster_wf.fill_team_rosters()
    standings_wf.run()

    return 0

if __name__ == '__main__':
    main()


