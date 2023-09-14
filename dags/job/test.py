from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from time import tzset
from UnleashClient import UnleashClient

tzset()

schedule = "0 0 * * *"

with DAG(dag_id="testtt",
         description="testtt",
         start_date=datetime.now() - timedelta(days=1),
         tags=["testtt"],
         schedule_interval=schedule) as dag:

    @task()
    def testtt():
        client = UnleashClient(
            url="http://unleash-web:4242/api/",
            app_name="default",
            environment="development",
            project_name="default",
            custom_headers={'Authorization': 'default:development.unleash-insecure-api-token'})
    
        client.initialize_client()
        
        test = client.get_variant("NOTION_BASE_URL")["payload"]["value"]
        print(test)
        
        
    testtt() 
