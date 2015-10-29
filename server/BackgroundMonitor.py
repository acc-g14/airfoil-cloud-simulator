

class BackgroundMonitor:

    def __init__(self, app):
        self._state = app.events.State()
        with app.connection() as connection:
            recv = app.events.Receiver(connection, handlers={
                'task-failed': self.announce_failed_tasks,
                'task-succeeded': self.task_succeeded,
                'worker-online': self.worker_online,
                'worker-heartbeat': self.worker_heartbeat,
                'worker-offline': self.worker_offline
            })
        recv.capture(limit=None, timeout=None, wakeup=True)

    def announce_failed_tasks(self, event):
        self._state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = self._state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def worker_online(self, event):
        self._state.event(event)
        print self._state
        print "Worker online"

    def worker_heartbeat(self, event):
        self._state.event(event)
        print "Heartbeat"

    def worker_offline(self, event):
        self._state.event(event)
        print "Worker offline"

    def task_succeeded(self, event):
        self._state.event(event)
        print "Successful task"
