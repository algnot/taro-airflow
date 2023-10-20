from dotenv import load_dotenv
import os
from UnleashClient import UnleashClient
from requests import patch
import json


class Config:
    client = UnleashClient(
      url="http://unleash-web:4242/api/",
      app_name="default",
      environment="development",
      project_name="default",
      custom_headers={'Authorization': os.environ["INIT_CLIENT_API_TOKENS"]})
    
    def __init__(self):
      load_dotenv()
      self.client.initialize_client()
      
    def get(self, name, defualt=""):
      try:
        value = self.client.get_variant(name) 
        
        if "payload" in value and "value" in value["payload"]:
          print(f"Get config {name} from unleash")
          return value["payload"]["value"]
        
        elif name in os.environ:
          print(f"Get config {name} from env value")
          return os.environ[name]
        
        print(f"Get config {name} from defualt value")
        return defualt
        
      except Exception as e:
        print(e)
        if name in os.environ:
          print(f"Get config {name} from env value")
          return os.environ[name]
        
        print(f"Get config {name} from defualt value")
        return defualt   
      
    def set(self, name, value):
      url = f"http://unleash-web:4242/api/admin/projects/default/features/{name}/environments/development/variants"
      
      payload = json.dumps([
        {
          "op": "replace",
          "path": "/0/payload/value",
          "value": value
        }
      ])
      
      api_key = self.get("UNLEASH_ADMIN_API_KEY")
      
      res = patch(url=url, headers={
        "Authorization": api_key,
        "Content-Type": "application/json"
      }, data=payload)
      
      if res.status_code != 200:
        raise Exception(f"Can not set config {name} status code {res.status_code} {url} {payload}")
      
      return res
    