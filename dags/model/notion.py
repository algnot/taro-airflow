from .config import Config
from requests import post, patch


class Notion():
    token = ""
    database_id = ""
    base_url = ""
    
    def __init__(self):
        config = Config()
        self.token = config.get("NOTION_TOKEN")
        self.database_id = config.get("NOTION_DATABASE_ID")
        self.base_url = config.get("NOTION_BASE_URL")
        
    def query(self, filter):
        url = self.base_url + "/v1/databases/" + self.database_id + "/query"
        query = { 
            "filter": filter 
        }
        res = post(url=url, json=query, headers={
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        })
        return res.json()["results"]
    
    def update(self, page_id, properties):
        url = self.base_url + "/v1/pages/" + page_id
        data = {
            "properties": properties
        }
        res = patch(url=url, json=data, headers={
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        })
        return res.json()
    