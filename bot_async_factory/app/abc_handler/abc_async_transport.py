import os
import json
import redis.asyncio as redis
from typing import List, Dict
from abc_handler.handlers import UniversalHandler
import abc_handler.config_queue as config_queue
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

class AbstractConnectorAsync:
    def __init__(self, redis_host=redis_host, redis_port=redis_port, handlers: List[UniversalHandler] = None):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_client = redis.Redis(host=redis_host,port=redis_port)  
        self.handlers = handlers or []
        self.queues = config_queue.QUEUES

    def register_handler(self, handler: UniversalHandler):
        self.handlers.append(handler)

    async def setup(self):
        self.redis_client = await self.redis_client.from_url(
            f'redis://{self.redis_host}:{self.redis_port}'
        )
        # Check connection
        try:
            await self.redis_client.ping()
            logger.info("Connected to Redis at {}:{}".format(self.redis_host, self.redis_port))
            await self.redis_client.aclose()
        except Exception as e:
            print(f'The exception: {e!r}')
            logger.error("Failed to connect to Redis at {}:{} due to: {}".format(self.redis_host, self.redis_port, e))
            raise

    async def run(self):
        await self.setup()
        while True:
            message = await self.redis_client.brpop(self.queues)
            source = message[0].decode('utf-8') 
            data = message[1] 
            await self.receive_message(source, data)

    async def receive_message(self, source: str, message: bytes):
        message_dict = self.parse_message(message)
        message_dict['source'] = source
        for handler in self.handlers:
            if handler.check(message_dict):
                logger.info(f"Handler {handler.__class__.__name__} will process the message")
                response = handler.process(message_dict)
                await self.get_message(response)

    async def get_message(self, response: Dict):
        """Message from handler given to inheritor"""
        raise NotImplementedError              

    async def push_message(self, response: Dict):
        queue_name = f"default"
        try:
            # Prepare the message data for Redis
            if isinstance(response, dict):
                print(f"response : Dict")
                response_source = response.get('source') or queue_name
                queue_name = f"{response_source}"
                message_data = json.dumps(response)
            elif isinstance(response, str):
                print(f"response : Str")
                message_data = response
            else:
                logger.error(f"Unsupported type of response: {type(response)}")
                return
            # Send the message to Redis queue
            print(f"{queue_name}:{response}")
            await self.redis_client.lpush(queue_name, message_data)
            logger.info(f"Message put into '{queue_name}' queue.")
        except Exception as e:
            logger.error(f"Failed to send message to {queue_name}: {e}")

    @staticmethod
    def parse_message(message: bytes) -> Dict:
        return json.loads(message.decode('utf-8'))




