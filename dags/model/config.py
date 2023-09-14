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
      self.client.initialize_client()
      
    def get(self, name, defualt=""):
      try:
        value = self.client.get_variant(name) 
        print(value)
        
        if "payload" in value and "value" in value["payload"]:
          print(f"Get config {name} from unleash")
          return value["payload"]["value"]
        
        elif name in os.environ:
          print(f"Get config {name} from env value")
          return os.environ[name]
        
      except Exception as e:
        print(e)
        if name in os.environ:
          print(f"Get config {name} from env value")
          return os.environ[name]
        
        print(f"Get config {name} from defualt value")
        return defualt   
    