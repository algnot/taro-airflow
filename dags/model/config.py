from dotenv import load_dotenv
import os
from UnleashClient import UnleashClient


class Config:
    client = UnleashClient(
      url="http://unleash-web:4242/api/",
      app_name="default",
      environment="development",
      project_name="default",
      custom_headers={'Authorization': os.environ["INIT_CLIENT_API_TOKENS"]})
    
    def __init__(self):
      load_dotenv()
      client.initialize_client()
      
    def get(self, name, defualt=""):
      try:
        value = client.get_variant(name) 
        
        if "payload" in value and "value" in value["payload"]:
          return value["payload"]["value"]
        
        elif name in os.environ:
          return os.environ[name]
        
      except Exception:
        if name in os.environ:
          return os.environ[name]
        
        return defualt   
    