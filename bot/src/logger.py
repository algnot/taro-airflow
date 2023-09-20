from requests import post
import os
import datetime
from dotenv import load_dotenv
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


class Logger:
  _name = "Logger"
  
  def warning(self, message):    
    self.send_message_to_webhook("Warning Message", message, "warning")
    
  def info(self, message):
    self.send_message_to_webhook("Info Message", message, "info")
    
  def error(self, message):
    self.send_message_to_webhook("Error Message", message, "error")
    
  def notify(self, message):
    self.send_message_to_webhook("Tongla x Notion", message, "notify")
    
  def get_webhook(self, level):
    config = Config()
    webhook_mapped = {
      "warning": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
      "info": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
      "error": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
      "notify": config.get("DISCORD_TONGLA_NOTION_WEBHOOK_URL")
    }
    
    try:
      return webhook_mapped[level]
    except Exception:
      return Exception(f"Webhook not found for level {level}")
    
  def get_color(self, level):
    color_mapped = {
      "warning": 15105570,
      "info": 3447003,
      "error": 15158332,
      "notify": 3447003
    }
    
    try:
      return color_mapped[level]
    except Exception:
      return Exception(f"Color not found for level {level}")
  
  def send_message_to_webhook(self, topic, message, level):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
      post(url=self.get_webhook(level), json={
        "embeds": [
          {
            "title": topic,
            "description": message,
            "color": self.get_color(level),
          },
        ],
      })
      print(f"[{level}] topic={topic} message={message} date={now} ")
    except Exception:  
      print(f"[{level}] topic={topic} message={message} date={now} ")
