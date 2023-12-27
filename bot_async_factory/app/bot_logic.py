
import asyncio
from typing import List, Dict
from abc_handler.abc_async_transport import AbstractConnectorAsync
from abc_handler.handlers import HiHandler, EchoHandler


class BotLogic(AbstractConnectorAsync):
    def __init__(self):
        super().__init__()
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())

    async def get_message(self, response: Dict):
        """Get message for work from redis queue."""
        print(f"Response:{response} from redis queue name '{response['source']}' ")
        # do some logic here
        if response['source'] == 'telegram':
            response['text'] = f"{response['text']} changed"
        if response['source'] == 'discord':
            response['content'] = f"{response['content']} changed"    
        # next push back to redis to pick up by client app
        """Push ready message from work to redis queue 'name'_send ."""
        response['source'] = f"{response['source']}_send"
        await self.push_message(response)    
        
if __name__ == "__main__":
    bot_logic = BotLogic()
    asyncio.run(bot_logic.run())


