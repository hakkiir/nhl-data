# repository.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from exceptions import SaveToDatabaseError
import pandas as pd

class DatabaseManager:
    def __init__(self, engine: engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def save(self, data: pd.DataFrame, table_name: str):
        session = self.Session()
        try:
            with self.engine.begin() as conn:
                data.to_sql(table_name, con=conn, if_exists="append", index=False)
                print(f">>> Data stored to {table_name}")
        except Exception as e:
            print(">>> Something went wrong while saving to db!")
            raise SaveToDatabaseError(f"Error: {e}") from e
        
        finally:
            session.close()


    def save_franchise_data(self, data: pd.DataFrame):
        self.save(data, "franchise")
    
    def save_teams_data(self, data: pd.DataFrame):
        self.save(data, "teams")