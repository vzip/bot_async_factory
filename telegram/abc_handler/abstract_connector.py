
import os
import redis
import json
from typing import List, Dict
from abc_handler.handlers import UniversalHandler

from loguru import logger
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

class AbstractConnector:
    def __init__(self, redis_host=redis_host, redis_port=6379, handlers: List[UniversalHandler] = None):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port)
            # Проверка подключения к Redis
            self.redis_client.ping()
            logger.info("Success Redis on {}:{}".format(redis_host, redis_port))
        except redis.ConnectionError:
            logger.error("Fail Redis on {}:{}".format(redis_host, redis_port))
            raise
        self.handlers = handlers or []
        self.queues = ['telegram_send']
        

    def register_handler(self, handler: UniversalHandler):
        self.handlers.append(handler)

    def run(self):
        """Start listening for messages from different queues and process them with registered handlers."""
        while True:
            # Listen to multiple queues
            source, message = self.redis_client.brpop(self.queues)
            self.receive_message(source, message)

    def receive_message(self, source: bytes, message: bytes):
        """Receive a message and process it with the appropriate handler."""
        source = source.decode('utf-8')  # Decode source from bytes to string
        message_dict = self.parse_message(message)
        # add source information to the message dict
        message_dict['source'] = source
        for handler in self.handlers:
            if handler.check(message_dict):
                logger.info(f"Handler {handler.__class__.__name__} will process the message")
                response = handler.process(message_dict)
                self.send_response(response)
                break


    def send_response(self, response: Dict):
        """Send a response message to the chat service."""
        # return response
        raise NotImplementedError        
    
    def send_message(self, message: Dict):
        """Send a response message to Redis."""
        if message['source'] == 'discord':
            self.redis_client.lpush('discord_send', json.dumps(message))
            logger.info("Send Discord message to Redis")
        elif message['source'] == 'telegram':
            self.redis_client.lpush('telegram_send', json.dumps(message))
            logger.info("Send Telegram message to Redis ")

    @staticmethod
    def parse_message(message: bytes) -> Dict:
        """Convert message from bytes to dict."""
        return json.loads(message.decode('utf-8'))

# This class is meant to be subclassed by specific connectors which implement the send_response method.

