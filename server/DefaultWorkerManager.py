from uuid import UUID
import uuid
from novaclient.exceptions import NotFound
import time
from WorkerManager import WorkerManager
from novaclient.client import Client
from utils import server_ip, DBUtil


class DefaultWorkerManager(WorkerManager):

    MAX_NUMBER = 10

    def __init__(self, config, db_name):
        WorkerManager.__init__(self)
        self._db_name = db_name
        DBUtil.execute_command(db_name,
                               "CREATE TABLE IF NOT EXISTS Workers " +
                               "(id text PRIMARY KEY, name text, initialized boolean, started DATETIME, starttime float, heartbeat DATETIME, active DATETIME)")
        self._config = config
        self._nc = Client('2', **config.nova_config)

    def get_max_number_of_workers(self):
        return self._config.max_workers

    def get_min_number_of_workers(self):
        return self._config.min_workers

    def get_number_of_workers(self):
        return DBUtil.execute_command(self._db_name, "SELECT COUNT(*) FROM Workers", None, "ONE")[0]

    def set_workers_available(self, num):
        available_workers = self.get_number_of_workers()
        # select either number or if number > max_workers use max_workers
        max_workers = min(num, self.get_max_number_of_workers())
        # always leave one worker available
        min_workers = max(max_workers, self.get_min_number_of_workers())
        if available_workers < max_workers:
            self._start_workers(max_workers - available_workers)
        elif available_workers > min_workers:
            self._shutdown_workers(available_workers - min_workers)

    def _start_workers(self, num):
        # basic parameters
        image = self._nc.images.find(name="G14Worker")
        flavor = self._nc.flavors.find(name="m1.medium")
        cloud_init = "#!/bin/bash \n" + \
                     " cd /home/ubuntu/airfoil-cloud-simulator \n" + \
                     "git reset --hard && git pull \n" + \
                     "echo '" + self._config.key + "' >> key.aes\n" + \
                     "echo '" + self._config.iv + "' >> iv.txt\n"\
                     " su -c 'celery -A workertasks worker -b amqp://cloudworker:worker@" + \
                     server_ip() + "//' ubuntu"
        for i in xrange(0, int(num)):
            name = "g14worker" + str(uuid.uuid1())
            server = self._nc.servers.create(name, image, flavor, userdata=cloud_init)
            DBUtil.execute_command(self._db_name,
                                   "INSERT INTO Workers(id, name, initialized, started, active) VALUES (?,?, 'false', ?, ?)",
                                   (server.id, name, time.time(), time.time()))

    def _shutdown_workers(self, num_workers):
        ids = DBUtil.execute_command(self._db_name, "SELECT id FROM Workers", None, num_workers)
        for row in ids:
            serverid = row[0]
            self._delete_worker(serverid)

    def _delete_worker(self, workerid):
        if self.get_number_of_workers() > self.get_min_number_of_workers():
            try:
                DBUtil.execute_command(self._db_name, "DELETE FROM Workers WHERE id = ?", (workerid,))
                self._nc.servers.find(id=workerid).delete()
            except NotFound:
                print "worker is not-existent"
            
    def delete_inactive_workers(self):
        results = DBUtil.execute_command(self._db_name, "SELECT id FROM Workers WHERE initialized = 'true' AND active <  ?", (time.time() - 60.0,), "ALL")
        for result in results:
            self._delete_worker(result[0])

    def delete_terminated_workers(self):
        DBUtil.execute_command(self._config.db_name,
                               "DELETE FROM Workers WHERE initialized = 'true' AND heartbeat < ?", (time.time() - 60.0,))