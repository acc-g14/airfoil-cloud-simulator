from utils import DBUtil

class BackgroundMonitor:

    def __init__(self, app, config):
        self._state = app.events.State()
        self._config = config
        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={
                'task-failed': self.announce_failed_tasks,
                'task-succeeded': self.task_succeeded,
                'worker-online': self.worker_online,
                'worker-heartbeat': self.worker_heartbeat,
                'worker-offline': self.worker_offline
            })
            recv.capture(limit=None, timeout=None, wakeup=True)

    def worker_online(self, event):
        self._state.event(event)
        name = event['hostname'].split("@")[1]
        DBUtil.execute_command(self._config.db_name, "UPDATE Workers SET initialized = 'true' WHERE name = ? ", (name,))
        print DBUtil.execute_command(self._config.db_name, "SELECT COUNT(*) FROM Workers", None, "ONE")[0]

    def worker_heartbeat(self, event):
        self._state.event(event)
        for key, worker in self._state.workers.iteritems():
            print key
            if not worker.alive:
                self._delete_worker_by_hostname(key)
        print self._state.workers

    def worker_offline(self, event):
        self._state.event(event)
        name = event['hostname'].split("@")[1]

    def task_succeeded(self, event):
        hash_key = event['uuid']
        result = event['result']
        DBUtil.execute_command(self._config.db_name, "INSERT INTO Result(name, value) VALUES(?,?)", (hash_key, result))

    def _delete_worker_by_hostname(self, hostname):
        name = hostname.split("@")[1]
        DBUtil.execute_command(self._config.db_name, "DELETE FROM Workers WHERE name = ?", (name,))
        return True
