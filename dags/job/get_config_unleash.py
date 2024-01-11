from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.config import Config
from time import tzset
from common.handle_error import handle_error
from model.logger import Logger
import os
import json

tzset()


with DAG(dag_id="get_config_unleash",
         description="Get config for unleash",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["dev"]) as dag:
    
    config = Config()
    logger = Logger()
    
    @task()
    @handle_error
    def get_config_unleash(*args, **kwargs):
        all_env = os.environ
        features = []
        feature_strategies = []
        feature_environments = []
        for key in all_env:
            if all_env[key]:
                features.append({
                    "name": key,
                    "description": None,
                    "type": "release",
                    "project": "default",
                    "stale": False,
                    "impressionData": False,
                    "archived": False
                })
                
                feature_strategies.append({
                    "name": "default",
                    "id": key,
                    "featureName": key,
                    "title": None,
                    "parameters": {},
                    "constraints": [],
                    "variants": [],
                    "disabled": False,
                    "segments": []
                })
                
                feature_environments.append({
                    "enabled": True,
                    "featureName": key,
                    "environment": "development",
                    "variants": [
                        {
                        "name": key,
                        "weight": 1000,
                        "payload": { "type": "string", "value": all_env[key]},
                        "overrides": [],
                        "stickiness": "default",
                        "weightType": "variable"
                        }
                    ],
                    "name": key
                })
            
        result = {
            "features": features,
            "featureStrategies": feature_strategies,
            "featureEnvironments": feature_environments,
            "contextFields": [],
            "featureTags": [],
            "segments": [],
            "tagTypes": [],
            "dependencies": []
        }        
        result = json.dumps(result)
        
        print(f"\n.\n.\n.\n.\n{result}\n.\n.\n.\n.\n")
        
    
    get_config_unleash()