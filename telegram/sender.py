import requests
from typing import List, Dict
from abc_handler.abstract_connector import AbstractConnector
from abc_handler.handlers import HiHandler, EchoHandler
import os

from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')

class BotSender(AbstractConnector):
    def __init__(self):
        super().__init__()
        print(f"token {telegram_token}")
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())
        
    def send_response(self, response: Dict):
        """Send a response message to the chat service."""
        print(f"message {response}")
        if 'chat_id' in response:
            chat_id = response['chat_id']
            text = response['text']
            # Call method to send message back to Telegram user
            self.send_message(chat_id=chat_id, text=text)
        else:
            return    
         
    def send_message(self, chat_id: str, text: str):
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        requests.post(url, json=payload)

if __name__ == "__main__":
    bot_logic = BotSender()
    bot_logic.run()



