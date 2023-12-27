
import telegram
from telegram import Update, constants, Bot 
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram.request import HTTPXRequest
from typing import List, Dict
import asyncio
import json
import os
from abc_handler.abc_async_transport import AbstractConnectorAsync
from abc_handler.handlers import HiHandler, EchoHandler
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))


class TelegramBot(AbstractConnectorAsync):
    def __init__(self):
        super().__init__()
        # create instance for transport
        self.abc_transport = AbstractConnectorAsync(redis_host=redis_host, redis_port=redis_port)
        # important to register_handler before application
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())
        # build instance for telegram
        self.application = ApplicationBuilder() \
            .token(telegram_token) \
            .connect_timeout(30) \
            .read_timeout(30) \
            .write_timeout(30) \
            .get_updates_request(HTTPXRequest(http_version="1.1")) \
            .http_version('1.1') \
            .build()      

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle messages from a Telegram bot and push them to a queue for making some logic out"""
        print(f'Handle message from telegram bot')
        data = {
            'chat_id': update.message.chat_id,
            'text': update.message.text,
            'source': f"telegram"
        }
        await self.abc_transport.push_message(data) 
        print(f'Message sent to Redis queue name : {data["source"]}')

    async def get_message(self, response: Dict):
        """Pick up message from queue and send to the telegram chat."""
        print(f"Success pick up message {response}")
        # Send message by Telegram client 
        chat_id = response['chat_id']
        text = response['text']
        await self.send_to_telegram(chat_id, text)     

    async def send_to_telegram(self, chat_id, text):
        await self.application.bot.send_message(chat_id, text)

    async def bootstrap(self) -> None:
        """Set up the application."""
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.prompt))
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)
        # AbstractConnectorAsync(run) after application 
        await self.run()
      
       
    async def start_task(self):
        """core"""
        await self.bootstrap()    
        

if __name__ == "__main__":
    bot_logic = TelegramBot()
    asyncio.run(bot_logic.start_task())