from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from model.logger import Logger
from model.notion import Notion
from model.common import get_next_datetime_schedule_by_schedule
import os
import time

os.environ["TZ"] = "Asia/Bangkok"
time.tzset()

schedule = "5 0 * * * *"

with DAG(dag_id="update_notion_status_job",
         description="Sync Notion Status Job",
         start_date=datetime.now(),
         tags=["notion"],
         schedule=schedule) as dag:

    logger = Logger()

    @task()
    def notify_start_job():
        logger.info("🐶 Start Update Notion Status Job")

    @task()
    def update_notion_status_job():
        try:
            update_notion_status()
        except Exception as e:
            logger.error(f"Error when update notion status: {e}")
            raise e

    def update_notion_status():
        notion = Notion()
        today = datetime.now()
        
        results = notion.query({
            "and": [
                {
                    "property": "Date",
                    "date": {
                        "before": today.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                    }
                },
                {
                    "or": [
                        {
                            "property": "Status",
                            "status": {
                                "equals": "Confirm"
                            }
                        },
                        {
                            "property": "Status",
                            "status": {
                                "equals": "In progress"
                            }
                        },
                        {
                            "property": "Status",
                            "status": {
                                "equals": "Planned"
                            }
                        }
                    ]
                }
            ]
        })
                
        message = ""
        inprogress_message = ""
        
        for result in results:
            page_id = result["id"]
            start_date = result["properties"]["Date"]["date"]["start"]
            end_date = result["properties"]["Date"]["date"]["end"]
            selected_date = end_date if end_date else start_date            
            status = "Done"
            
            if "T" in selected_date:
                selected_date = selected_date.split("T")[0]
            
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
                        
            if(selected_date < today):
                status = "In progress"
                name = result["properties"]["Name"]["title"][0]["plain_text"]
                date = selected_date
                public_url = result["public_url"]
                inprogress_message += f"- [{name}]({public_url}) ending at `({date})`)\n"
                
            if result["properties"]["Status"]["status"]["name"] == "Planned":
                status = "Cancel"
                
            properties = {
                "Status": {
                    "status": {
                        "name": status,
                    },
                },
            };
            
            notion.update(page_id, properties)
            message += f"- Updated card (`{page_id}`) to `{status}`.\n";
            
        if message:
            logger.info(f"{message}\n\n🐶 dataDone={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            logger.warning(f"🐶 Not have update card\n\ndataDone={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
        if inprogress_message:
            logger.notify(f"Tomorrow task ({selected_date})\n{inprogress_message}")
            
    notify_start_job() >> update_notion_status_job()
