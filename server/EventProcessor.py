from celery.result import AsyncResult
import time
from storage.DatabaseStorage import DatabaseStorage
from utils import DBUtil


class EventProcessor:
    """
    Class which should be executed as background task. Updates task results and keeps track of workers going on-
    or offline.
    """

    def __init__(self, app, config):
        try:
            self._state = app.events.State()
            self._config = config
            self._storage = DatabaseStorage(config.db_name)
            self._init_event_receiver(app)
        except KeyboardInterrupt:
            # return gracefully.
            pass

    def worker_online(self, event):
        """
        Event handler when worker comes online.
        :param event:
        """
        self._state.event(event)
        name = event['hostname'].split("@")[1]
        init_time = event['timestamp']
        result = DBUtil.execute_command(self._config.db_name, "SELECT started FROM Workers WHERE name = ?", (name,), "ONE")
        if result is not None:
            starttime = init_time - result[0]
            print "STARTTIME: " + str(starttime)
            DBUtil.execute_command(self._config.db_name, "UPDATE Workers SET initialized = 'true', starttime = ?, heartbeat = ?  WHERE name = ? ", (starttime, time.time(), name))

    def worker_heartbeat(self, event):
        """
        Event handler for received heartbeat from a worker
        :param event:
        """
        hostname = event['hostname']
        if "active" in event:
            print "active found"
            self._update_worker(hostname, event['active'])
        else:
            self._update_worker(hostname)


        # check for offline workers and delete them from the database
        for key, worker in self._state.workers.iteritems():
            if not worker.alive:
                self._delete_worker_by_hostname(key)

    def worker_offline(self, event):
        """
        Event handler when worker goes offline.
        :param event:
        """
        self._state.event(event)
        name = event['hostname']
        self._delete_worker_by_hostname(name)

    def task_started(self, event):
        self._state.event(event)
        hash_key = event['uuid']
        started = event['timestamp']
        print "task started"
        DBUtil.execute_command(self._config.db_name, "UPDATE Results SET started = ? WHERE name = ?", (started, hash_key))

    def task_succeeded(self, event):
        """
        Event handler when task succeeds
        :param event:
        """
        self._state.event(event)
        hash_key = event['uuid']
        endtime = event['timestamp']
        asyncresult = AsyncResult(hash_key)
        self._storage.save_result_hash(hash_key, asyncresult.get(), None, endtime)
        print "Task succeeded:" + hash_key

    def _delete_worker_by_hostname(self, hostname):
        """
        Internal method to delete worker from database by using its hostname
        :param hostname:
        :return:
        """
        name = hostname.split("@")[1]
        DBUtil.execute_command(self._config.db_name, "DELETE FROM Workers WHERE name = ?", (name,))

    def _init_event_receiver(self, app):
        """
        Internal method to allow event handling.
        :param app:
        :return:
        """
        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={
                'task-succeeded': self.task_succeeded,
                'task-started': self.task_started,
                'worker-online': self.worker_online,
                'worker-heartbeat': self.worker_heartbeat,
                'worker-offline': self.worker_offline
            })
            recv.capture(limit=None, timeout=None, wakeup=True)

    def _update_worker(self, hostname, active=0):
        name = hostname.split("@")[1]
        heartbeat = time.time()
        if active > 0:
            DBUtil.execute_command(self._config.db_name, "UPDATE Workers SET heartbeat = ?, last_active = ? WHERE name = ?", (heartbeat, heartbeat, name))
        else:
            DBUtil.execute_command(self._config.db_name, "UPDATE Workers SET heartbeat = ? WHERE name = ?", (heartbeat, name))