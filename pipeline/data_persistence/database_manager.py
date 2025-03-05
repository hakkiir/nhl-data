# repository.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine, select, MetaData
from pipeline.exceptions import SaveToDatabaseError
import pandas as pd
import logging
import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, engine: engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        self._metadata = MetaData()
        self._metadata.reflect(engine)

    def load(self, df: pd.DataFrame, table_name: str):
        session = self.Session()
        try:
            with self.engine.begin() as conn:
                df.to_sql(table_name, con=conn, if_exists='append', index=False, method=postgres_upsert)
                print(f">>> Data stored to {table_name}")
                logger.info(f"{datetime.datetime.now()} : Data stored to {table_name}")
        except Exception as e:
            print(">>> Something went wrong while saving to db!")
            raise SaveToDatabaseError(f"Error: {e}") from e
        
        finally:
            session.close()


    def save_franchise_data(self, df: pd.DataFrame):
        self.load(df, "franchise")
    
    def save_teams_data(self, df: pd.DataFrame):
        self.load(df, "teams")

    def save_schedule_data(self, df: pd.DataFrame):
        self.load(df, "schedule")
    
    def save_roster_data(self, df: pd.DataFrame):
        self.load(df, "players")

    def get_teams_in_season(self) -> list:
        session = self.Session()
        teams = self._metadata.tables['teams']
        schedule = self._metadata.tables['schedule']
        stmt = select(teams.c.team_id, teams.c.raw_tricode).where(teams.c.team_id.in_(select(schedule.c.away_team_id).group_by(schedule.c.away_team_id)))
        output = []
        try:
            with self.engine.connect() as conn:
                for row in conn.execute(stmt):
                    output.append(row)
        except Exception as e:
            print(f">>> Something went wrong while retrieving from db!\n:{e}")
        finally:
            session.close()
        return output
    
def postgres_upsert(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    insert_statement = insert(table.table).values(data)
    upsert_statement = insert_statement.on_conflict_do_update(
        constraint=f"{table.table.name}_pkey",
        set_={c.key: c for c in insert_statement.excluded},
    )
    conn.execute(upsert_statement)