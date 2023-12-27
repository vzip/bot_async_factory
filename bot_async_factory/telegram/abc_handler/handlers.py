from typing import Dict

class UniversalHandler:
    def check(self, message: Dict) -> bool:
        """Check if the handler can process the message."""
        raise NotImplementedError

    def process(self, message: Dict) -> Dict:
        """Process the message and return a response."""
        raise NotImplementedError

class HiHandler(UniversalHandler):
    def check(self, message: Dict) -> bool:
        return message.get('text', '').startswith('/hi')

    def process(self, message: Dict) -> Dict:
        return {'text': 'Hi'}

class EchoHandler(UniversalHandler):
    def check(self, message: Dict) -> bool:
        return True

    def process(self, message: Dict) -> Dict:
        return message

