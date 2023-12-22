import asyncio
import os
import sys
import creart
sys.path.append(os.getcwd())
from asyncio import AbstractEventLoop
from exithooks import hook
from loguru import logger
from telegram_transport import TelegramBot 

loop = creart.create(AbstractEventLoop)
bots = []
tg = TelegramBot()
bots.append(loop.create_task(tg.start_task()))

hook()
loop.run_until_complete(asyncio.gather(*bots))
loop.run_forever()