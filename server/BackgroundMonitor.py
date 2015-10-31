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
            # return gracefully.
            pass

    def do_some_work(self):
        avg_worker_time = self._get_average_worker_startup_time()
        num_current_workers = self._get_num_current_workers()
        current_queue_length = self._get_current_queue_length()
        avg_task_time = self._get_avg_task_time()
        print str(avg_worker_time)
        print str(current_queue_length)
        print str(num_current_workers)
        print str(avg_task_time)

    def _get_average_worker_startup_time(self):
        results = DBUtil.execute_command(self._config.db_name,
                                         "SELECT starttime FROM Workers WHERE starttime IS NOT NULL", None, "ALL")
        if len(results) > 0:
            result_sum = 0.0
            for result in results:
                result_sum += result[0]
            return result_sum / float(len(results))
        else:
            return 0.0

    def _get_current_queue_length(self):
        results = DBUtil.execute_command(self._config.db_name, "SELECT COUNT(*) FROM Results WHERE value IS NULL",
                                         None, "ONE")
        return results[0]

    def _get_num_current_workers(self):
        results = DBUtil.execute_command(self._config.db_name, "SELECT COUNT(*) FROM Workers", None, "ONE")
        return results[0]

    def _get_avg_task_time(self):
        results = DBUtil.execute_command(self._config.db_name, "SELECT runtime FROM Results WHERE runtime IS NOT NULL",
                                         None, "ALL")
        if len(results) > 0:
            result_sum = 0.0
            for result in results:
                result_sum += result[0]
            return result_sum / float(len(results))
        else:
            return 0.0
