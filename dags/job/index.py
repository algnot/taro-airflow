from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from model.logger import Logger
from model.notion import Notion
from time import tzset

tzset()

schedule = "5 0 * * *"

with DAG(dag_id="update_notion_status_job",
         description="Sync Notion Status Job",
         start_date=datetime.now() - timedelta(days=1), 
         tags=["notion", "discord"],        
         schedule_interval=schedule) as dag:

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
            current_status = result["properties"]["Status"]["status"]["name"]
            
            if "T" in selected_date:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%dT%H:%M:%S.000+07:00")
            else:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
            
            selected_date = selected_date.replace(hour=23, minute=59, second=59)
                                        
            if selected_date > today and current_status != "Planned":
                status = "In progress"
                name = result["properties"]["Name"]["title"][0]["plain_text"]
                date = selected_date
                public_url = result["public_url"]
                inprogress_message += f"- [{name}]({public_url}) ending at (`{date}`)\n"
                
            if current_status == "Planned":
                status = "Cancel"
                
            properties = {
                "Status": {
                    "status": {
                        "name": status,
                    },
                },
            };
            
            if status != current_status:
                notion.update(page_id, properties)
                message += f"- Updated `{page_id}` `{current_status}` -> `{status}`\n";
            
        if message:
            logger.info(f"{message}\n\n🐶 dataDone={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            logger.warning(f"🐶 Not have update card\n\ndataDone={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
        if inprogress_message:
            logger.notify(f"Tomorrow task ({today.strftime('%d/%m/%Y')})\n{inprogress_message}")
        else:
            logger.notify("Tomorrow you don't have any task 😃")
            
    notify_start_job() >> update_notion_status_job()
