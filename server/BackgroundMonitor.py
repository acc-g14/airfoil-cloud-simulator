from utils import DBUtil


class BackgroundMonitor:
    """
    Class which should be executed as background task. Updates task results and keeps track of workers going on-
    or offline.
    """

    def __init__(self, app, config):
        self._state = app.events.State()
        self._config = config
        self._init_event_receiver(app)

    def worker_online(self, event):
        """
        Event handler when worker comes online.
        :param event:
        """
        self._state.event(event)
        name = event['hostname'].split("@")[1]
        DBUtil.execute_command(self._config.db_name, "UPDATE Workers SET initialized = 'true' WHERE name = ? ", (name,))

    def worker_heartbeat(self, event):
        """
        Event handler for received heartbeat from a worker
        :param event:
        """
        self._state.event(event)
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
        name = event['hostname'].split("@")[1]
        self._delete_worker_by_hostname(name)

    def task_succeeded(self, event):
        """
        Event handler when task succeeds
        :param event:
        """
        hash_key = event['uuid']
        result = event['result']
        DBUtil.execute_command(self._config.db_name, "INSERT INTO Result(name, value) VALUES(?,?)", (hash_key, result))

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
                'worker-online': self.worker_online,
                'worker-heartbeat': self.worker_heartbeat,
                'worker-offline': self.worker_offline
            })
            recv.capture(limit=None, timeout=None, wakeup=True)