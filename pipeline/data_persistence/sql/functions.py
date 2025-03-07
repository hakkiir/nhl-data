from sqlalchemy import Engine
from database_manager import DatabaseManager

def fill_divisions_table(engine: Engine):
    db = DatabaseManager(engine)
    db.run_sql_file("insert_divisions")