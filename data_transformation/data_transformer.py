import pandas as pd
from typing import Dict, Any


class DataTransformer:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def transform(self, data: Dict[str, Any]):
        return self.strategy.transform(data)
    

class TeamsTransformationStrategy:
    def transform(self, data: Dict[str, Any]):
        df = pd.json_normalize(data["data"])
        return df