
from typing import List, Dict
from abc_handler.abstract_connector import AbstractConnector
from abc_handler.handlers import HiHandler, EchoHandler
import os
import json
import requests
from dotenv import load_dotenv
from loguru import logger
load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class BotSender(AbstractConnector):
    def __init__(self):
        super().__init__()
        print(f"token {discord_token}")
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())
        
    def send_response(self, response: Dict):
        """Send a response message to the chat service."""
        print(f"message {response}")
        if 'channel_id' in response:
            channel_id = response['channel_id']
            content = response['content']
            # Call method to send message back to Discord user
            self.send_to_discord(channel_id, content)
        else:
            return    
         
    def send_to_discord(self, channel_id, message):
        headers = {
            "Authorization": f"Bot {discord_token}",
            "Content-Type": "application/json"
        }
        data = {
            "content": message
        }

        response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=data)
        logger.info(f"Response: {response}")

if __name__ == "__main__":
    bot_logic = BotSender()
    bot_logic.run()
    



