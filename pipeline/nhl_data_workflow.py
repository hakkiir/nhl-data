from typing import Optional, Dict, Any
import logging
from sqlalchemy.engine import Engine
from pandas import DataFrame
from .data_fetching import DataFetchFactory, DataFetcher
from .data_transformation import (
    DataTransformer, 
    ScheduleTransformationStrategy,
    TeamsTransformationStrategy,
    RosterTransformationStrategy,
    FranchiseTransformationStrategy)
from .data_persistence import DatabaseManager
from pipeline.exceptions import SaveToDatabaseError

class NHLDataWorkflow():

    def __init__(
        self, 
        fetcher: DataFetcher, 
        transformer: DataTransformer, 
        database_manager: DatabaseManager,
        table_name: str,
        name: Optional[str] = None,
    ):

        """
        :param fetcher: Data fetching component
        :param transformer: Data transformation component
        :param database_manager: Database management component
        :param table_name: name of the table that dbmanager loads to
        :param name: Optional name for the pipeline (useful for logging)
        """
        self.fetcher = fetcher
        self.transformer = transformer
        self.database_manager = database_manager
        self.table_name = table_name
        self.name = name
        self.backfill_generator = None
        # Configure logging
        self.logger = logging.getLogger(name or self.__class__.__name__)
        
        # Pipeline state tracking
        self.raw_data = None
        self.transformed_data = None
    
    def fetch(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch raw data using the associated fetcher.
        :return: Fetched data
        """
        try:
            self.logger.info(f"Starting data fetch from endpoint: {self.fetcher.endpoint}, params: {kwargs}")
            self.raw_data = self.fetcher.fetch(**kwargs)
            self.logger.info("Data fetch completed successfully")
            return self.raw_data
        except Exception as e:
            self.logger.error(f"Data fetch failed: {e}")
            raise

    def backfill(self) -> int:
        try:
            self.logger.info(f"Creating backfill generator: {self.fetcher.endpoint}")
            self.backfill_generator = self.fetcher.backfill_generator()
            for self.raw_data in self.backfill_generator:
                self.logger.info("fetching..")
                self.logger.info("transforming..")
                self.transform()
                self.logger.info("loading..")
                try:
                    self.load()
                except SaveToDatabaseError as e:
                    self.logger.error(f"backfill error: {e}")
            
            return 0
        except Exception as e:
            self.logger.error(f"Data backfill failed: {e}")
            raise

    def transform(self, **kwargs) -> DataFrame:
        """
        Transform raw data using the associated transformer.
        :return: Transformed data
        """
        if self.raw_data is None:
            raise ValueError("No raw data available. Call fetch() first.")
        
        try:
            self.logger.info("Starting data transformation")
            self.transformed_data = self.transformer.transform(self.raw_data, **kwargs)
            self.logger.info("Data transformation completed successfully")
            return self.transformed_data
        except Exception as e:
            self.logger.error(f"Data transformation failed: {e}")
            raise
    
    def load(self):
        """
        Load transformed data into the database.
         :return: Result of database operation
        """
        if self.database_manager is None:
            self.logger.warning("No database manager configured. Skipping load.")
            return None
        
        if self.transformed_data is None:
            raise ValueError("No transformed data available. Call transform() first.")
    
        try:
            self.logger.info("Starting data loading")
            result = self.database_manager.load(self.transformed_data, self.table_name)
            self.logger.info("Data loading completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            raise
    
    def run(self):
        """
        Execute the entire pipeline: fetch -> transform -> load.
        
        :return: Loaded data or transformation result
        """
        try:
            self.logger.info("Starting full pipeline execution")
            self.fetch()
            self.transform()
            return self.load()
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {e}")
            raise
    
    def reset(self):
        """
        Reset the pipeline state.
        """
        self.raw_data = None
        self.transformed_data = None
        self.logger.info("Pipeline state reset")


# Concrete pipelines
def create_nhl_teams_pipeline(engine: Engine) -> NHLDataWorkflow:
    fetcher = DataFetchFactory.get_fetcher('teams')
    transformer = DataTransformer(strategy=TeamsTransformationStrategy())
    db_manager = DatabaseManager(engine)
    
    return NHLDataWorkflow(
        fetcher=fetcher, 
        transformer=transformer, 
        database_manager=db_manager,
        table_name='teams',
        name="NHL_Teams_Pipeline",
    )

def create_nhl_franchise_pipeline(engine: Engine) -> NHLDataWorkflow:
    fetcher = DataFetchFactory.get_fetcher('franchise')
    transformer = DataTransformer(strategy=FranchiseTransformationStrategy())
    db_manager = DatabaseManager(engine)
    
    return NHLDataWorkflow(
        fetcher=fetcher, 
        transformer=transformer, 
        database_manager=db_manager,
        table_name='franchise',
        name="NHL_Franchise_Pipeline",
    )

def create_nhl_roster_pipeline(engine: Engine) -> NHLDataWorkflow:
    fetcher = DataFetchFactory.get_fetcher('roster')
    transformer = DataTransformer(strategy=RosterTransformationStrategy())
    db_manager = DatabaseManager(engine)
   
    return NHLDataWorkflow(
        fetcher=fetcher,
        transformer=transformer,
        database_manager=db_manager,
        table_name='players',
        name="NHL_Roster_Pipeline",
    )

def create_nhl_schedule_backfill_pipeline(engine: Engine) -> NHLDataWorkflow:
    fetcher = DataFetchFactory.get_fetcher('schedule_backfill')
    transformer = DataTransformer(strategy=ScheduleTransformationStrategy())
    db_manager = DatabaseManager(engine)
   
    return NHLDataWorkflow(
        fetcher=fetcher,
        transformer=transformer,
        database_manager=db_manager,
        table_name='schedule',
        name="NHL_Schedule_Pipeline",
    )


def fill_team_rosters(workflow: NHLDataWorkflow) -> None:
    """
    Utility function to fill rosters for all teams in the current season.

    """
    teams = workflow.database_manager.get_teams_in_season()
    print(teams)
    # Track processing results
    successful_teams = []
    failed_teams = []
    
    for team in teams:
        team_id, tricode = team[0], team[1]
        
        try:
            print(f"fetching {tricode}")
            workflow.fetch(team_tricode=tricode)
            workflow.transform(current_team_id=team_id)
            workflow.load()
            workflow.reset()
            
            successful_teams.append(tricode)
            workflow.logger.info(f"Successfully processed roster for team {tricode}")
        
        except Exception as e:
            workflow.logger.error(f"Failed to process roster for team {tricode}: {e}")
            failed_teams.append((tricode, str(e)))
    
    # Summary logging
    workflow.logger.info(f"Roster fill completed. Successful: {len(successful_teams)}, Failed: {len(failed_teams)}")