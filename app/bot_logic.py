
from typing import List, Dict
from abc_handler.abstract_connector import AbstractConnector
from abc_handler.handlers import HiHandler, EchoHandler

class BotLogic(AbstractConnector):
    def __init__(self):
        super().__init__()
        self.register_handler(HiHandler())
        self.register_handler(EchoHandler())
        self.send_bot = AbstractConnector()

    def send_response(self, response: Dict):
        """Send a response message to the chat service."""
        print(f"message {response}")
        # Вызовите здесь метод отправки сообщения, например, через Redis
        self.send_bot.send_message(response)    

        
if __name__ == "__main__":
    bot_logic = BotLogic()
    bot_logic.run()

