import pipeline as pl
import os
import sqlalchemy as db
import argparse
import endpoint_urls as urls

parser = argparse.ArgumentParser()
parser.add_argument('--static', '-s', help="run pipelines for static data", type= bool, default= False)



def main() -> int:
    args = parser.parse_args()
    
    # db url from env and db connection
    dbUrl = os.getenv('DB_URL')
    engine = db.create_engine(dbUrl)

    # declare static-data pipeline objects
    franchise = pl.Franchise(urls.FRANCHISE_URL, engine)

    # decalre dynamic-data pipeline objects
    schedule = pl.Schedule(urls.SCHEDULE_URL, engine)

    #check static parameter and run static if true
    if args.static:
        franchise.run_pipeline()

    # run other
    schedule.run_pipeline()

    #p.run_pipeline()

    return 0

if __name__ == '__main__':
    main()