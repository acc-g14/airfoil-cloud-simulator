from WorkerManager import WorkerManager
from novaclient.client import Client
from netifaces import interfaces, ifaddresses, AF_INET


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
        min_workers = max(max_workers, 1)
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
                     " su -c 'celery -A workertasks worker -b amqp://cloudworker:worker@" + \
                     self._my_ip() + "//' ubuntu"
        for i in range(0, num):
            server = self.nc.servers.create("G14Worker" + str(i), image, flavor, userdata=cloud_init)
            self._workers.append(server)

    # from http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    @staticmethod
    def _my_ip():
        """
        :rtype : string
        """
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            if ifaceName == "eth0":
                return addresses[0]

    @staticmethod
    def _shutdown_workers(self, worker):
        # TODO: implement
        pass
