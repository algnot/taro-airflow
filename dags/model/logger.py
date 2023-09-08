from requests import post
import os
import datetime
from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
      load_dotenv()
      
    def get(self, name, defualt=""):
        if name in os.environ:
            return os.environ[name]
        
        return defualt


class Logger:
  _name = "Logger"
  
  def warning(self, message):    
    self.send_message_to_webhook("[Warning] Tongla x Notion", message, "warning")
    
  def info(self, message):
    self.send_message_to_webhook("[Info] Tongla x Notion", message, "info")
    
  def error(self, message):
    self.send_message_to_webhook("[Error] Tongla x Notion", message, "error")
    
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
