
import telegram
from telegram import Update, constants, Bot 
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram.request import HTTPXRequest
from typing import List, Dict
import redis
import json
import os
from abc_handler.abstract_connector import AbstractConnector
from abc_handler.handlers import HiHandler, EchoHandler
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

redis_client = redis.Redis(host=redis_host, port=redis_port)
print(f"token {telegram_token}")

class TelegramBot(AbstractConnector):
    def __init__(self):
        super().__init__()
        print(f"token {telegram_token}")
        self.application = ApplicationBuilder() \
            .token(telegram_token) \
            .connect_timeout(30) \
            .read_timeout(30) \
            .write_timeout(30) \
            .get_updates_request(HTTPXRequest(http_version="1.1")) \
            .http_version('1.1') \
            .build()    
        self.send_bot = AbstractConnector()
        self.send_bot.register_handler(HiHandler())
        self.send_bot.register_handler(EchoHandler())

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f'Handle message from telegram bot')
        data = {
            'chat_id': update.message.chat_id,
            'text': update.message.text
        }
        redis_client.lpush('telegram', json.dumps(data))
        print(f'Message sent to Redis telegram')

    async def send_to_telegram(self, chat_id, text):
        await self.application.bot.send_message(chat_id, text)

    async def bootstrap(self) -> None:
        """Set up the application."""
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.prompt))
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)
    
    async def start_task(self):
        """core"""
        await self.bootstrap()      

