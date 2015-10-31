import time
from model.Config import Config
from server.DefaultWorkerManager import DefaultWorkerManager
from utils import DBUtil


class BackgroundMonitor():

    def __init__(self):
        self._config = Config()
        self._worker_manager = DefaultWorkerManager(self._config, self._config.db_name)
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
        if current_queue_length > 0 and avg_task_time > 0.0 and avg_worker_time > 0.0 and num_current_workers > 0:
            #TODO: adjust calculation
            # assuming 2 threads to perform tasks per worker
            eta = current_queue_length * avg_task_time / (2*num_current_workers)
            num_additional_workers = 0
            print "eta: " + str(eta)
            print "worker startup: " + str(avg_worker_time)
            while eta > avg_worker_time:
                num_additional_workers += 1
                eta = current_queue_length * avg_task_time / (2*(num_current_workers + num_additional_workers))
            num_additional_workers -= 1
            print "Addtional workers: " + str(num_additional_workers)
            self._worker_manager.set_workers_available(num_additional_workers + num_current_workers)
            #TODO
            pass
        elif current_queue_length > 0 and num_current_workers == 0:
            self._worker_manager.set_workers_available(round(current_queue_length / 2))
        print str(avg_worker_time)
        print str(current_queue_length)
        print str(num_current_workers)
        print str(avg_task_time)

    def _get_average_worker_startup_time(self):
        DBUtil.execute_command(self._config.db_name,
                               "DELETE FROM Workers WHERE initialized = 'true' AND heartbeat < ?", (time.time() - 60.0,))
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
        results = DBUtil.execute_command(self._config.db_name, "SELECT COUNT(*) FROM Results WHERE value = 'null'",
                                         None, "ONE")
        return results[0]

    def _get_num_current_workers(self):
        return self._worker_manager.get_number_of_workers()

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
