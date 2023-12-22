import atexit
import sys
import os
from loguru import logger
import signal


class ExitHooks(object):
    def __init__(self):
        self._orig_exit = None
        self.exit_code = None
        self.exception = None

    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc, *args):
        self.exception = exc


hooks = ExitHooks()
hooks.hook()


def foo():
    if hooks.exit_code is not None or hooks.exception is not None:
        if isinstance(hooks.exception, (KeyboardInterrupt, type(None))):
            return
        logger.error("It seems that the program did not exit normally.")
        logger.exception(hooks.exception)
        raise hooks.exception


atexit.register(foo)


def exit_gracefully(signal, frame):
    
    logger.warning("The program is about to exit...".format(signal))
    sys.exit(0)


def hook():
    signal.signal(signal.SIGINT, exit_gracefully)