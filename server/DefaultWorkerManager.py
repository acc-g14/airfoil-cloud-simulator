from WorkerManager import WorkerManager
from novaclient.client import Client
from utils import server_ip
import sqlite3


class DefaultWorkerManager(WorkerManager):

    MAX_NUMBER = 10

    def __init__(self, novaconfig, db_name):
        WorkerManager.__init__(self)
        self._workers = []
        self.db_name = db_name
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Workers (ip text PRIMARY KEY)")
        conn.commit()
        conn.close()
        self.nc = Client('2', **novaconfig)

    def get_max_number_of_workers(self):
        # TODO: add some config?
        return DefaultWorkerManager.MAX_NUMBER

    def get_number_of_workers(self):
        # TODO: respect workers which are currently starting/initializing
        return len(self._workers)

    def set_workers_available(self, num):
        print "Hallo"
        available_workers = self.get_number_of_workers()
        max_workers = min(num, self.get_max_number_of_workers())
        # always leave one worker available
        min_workers = max(max_workers, 0)
        if available_workers < max_workers:
            self._start_workers(max_workers - available_workers)
        elif available_workers > min_workers:
            self._shutdown_workers(available_workers - min_workers)

    def _start_workers(self, num):
        # basic parameters
        image = self.nc.images.find(name="G14Worker")
        flavor = self.nc.flavors.find(name="m1.medium")
        servers_to_init = []
        cloud_init = "#!/bin/bash \n" + \
                     " cd /home/ubuntu/airfoil-cloud-simulator \n" + \
                     "git reset --hard && git pull \n" + \
                     " su -c 'celery -A workertasks worker -b amqp://cloudworker:worker@" + \
                     server_ip() + "//' ubuntu"
        for i in xrange(0, num):
            server = self.nc.servers.create("G14Worker" + str(i), image, flavor, userdata=cloud_init)
            self._workers.append(server)

    def save_ips(self):
        for worker in self._workers:
            for key, network in worker.networks.iteritems():
                ip = network[0]
                self._save_ip(ip)
                break

    # from http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    def _save_ip(self, ip):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO Workers VALUES(?)", (ip,))
        conn.commit()
        conn.close()

    def _shutdown_workers(self, num_workers):
        for i in xrange(0, num_workers):
            self._workers.pop().delete()
        pass
