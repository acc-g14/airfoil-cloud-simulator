from threading import Thread
import time
from model.Config import Config
from utils import DBUtil


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
        avg_worker_time = self._get_average_worker_startup_time()

    def _get_average_worker_startup_time(self):
        results = DBUtil.execute_command(self._config.db_name, "SELECT starttime FROM Workers WHERE starttime != NULL", None, "ALL");
        for result in results:
            print result
        return results