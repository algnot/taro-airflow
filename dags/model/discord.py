from requests import post
from .config import Config

class Discord:
    config = Config()
    webhook = config.get("DISCORD_USICK_ALERT_WEBHOOK_URL")
    
    def __init__(self, webhook=False):
        if webhook:
            self.webhook = webhook
    
    def send_message(self, message):
        post(self.webhook, json={"content": message})
    