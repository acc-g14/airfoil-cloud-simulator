from threading import Thread
import time
from model.Config import Config


class BackgroundMonitor():

    def __init__(self):
        self._config = Config()
        try:
            while True:
                time.sleep(10)
                self.do_some_work()
        except KeyboardInterrupt:
            pass

    def do_some_work(self):
        pass