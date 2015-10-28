import novaclient.exceptions
from WorkerManager import WorkerManager
from novaclient.client import Client
from utils import server_ip
import sqlite3


class DefaultWorkerManager(WorkerManager):

    MAX_NUMBER = 10

    def __init__(self, config, db_name):
        WorkerManager.__init__(self)
        self._workers = []
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Workers (id text PRIMARY KEY)")
        conn.commit()
        conn.close()
        self._config = config
        self._nc = Client('2', **config.nova_config)

    def get_max_number_of_workers(self):
        return self._config.max_workers

    def get_min_number_of_workers(self):
        return self._config.min_workers

    def get_number_of_workers(self):
        return len(self._workers)

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
        for i in xrange(0, num):
            server = self._nc.servers.create("G14Worker" + str(i), image, flavor, userdata=cloud_init)
            self._workers.append(server)

    def save_ids(self):
        """
        Save known workers to database.
        :return:
        """
        for worker in self._workers:
            self._save_id(worker.id)

    def _save_id(self, wid):
        conn = sqlite3.connect(self._config.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO Workers VALUES(?)", (wid,))
        conn.commit()
        conn.close()

    def load_workers(self):
        """
        Recover workers saved in database.
        :return:
        """
        conn = sqlite3.connect(self._config.db_name)
        c = conn.cursor()
        c.execute("SELECT id FROM Workers")
        ids = c.fetchall()
        for wid in ids:
            self._load_worker(wid)
        c.execute("DELETE FROM Workers")
        conn.commit()
        conn.close()

    def _shutdown_workers(self, num_workers):
        for i in xrange(0, num_workers):
            self._workers.pop().delete()
        pass

    def _load_worker(self, wid):
        try:
            worker = self._nc.servers.find(id=wid)
            if worker is not None:
                self._workers.append(worker)
        except novaclient.exceptions.NotFound:
            pass
