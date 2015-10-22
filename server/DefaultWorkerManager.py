from WorkerManager import WorkerManager
from novaclient.client import Client
from utils import server_ip


class DefaultWorkerManager(WorkerManager):

    MAX_NUMBER = 10

    def __init__(self, novaconfig):
        WorkerManager.__init__(self)
        self._workers = []
        self.nc = Client('2', **novaconfig)

    def get_max_number_of_workers(self):
        # TODO: add some config?
        return DefaultWorkerManager.MAX_NUMBER

    def get_number_of_workers(self):
        # TODO: respect workers which are currently starting/initializing
        return len(self._workers)

    def set_workers_available(self, num):

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
        cloud_init = "#!/bin/bash \n" + \
                     " cd /home/ubuntu/airfoil-cloud-simulator \n" + \
                     "git reset --hard && git pull \n" + \
                     " su -c 'celery -A workertasks worker -b amqp://cloudworker:worker@" + \
                     server_ip() + "//' ubuntu"
        for i in range(0, num):
            server = self.nc.servers.create("G14Worker" + str(i), image, flavor, userdata=cloud_init)
            self._workers.append(server)

    # from http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

    def _shutdown_workers(self, num_workers):
        for i in xrange(0, num_workers):
            self._workers.pop().delete()
        pass
