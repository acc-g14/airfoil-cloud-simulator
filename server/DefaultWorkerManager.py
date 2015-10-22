from WorkerManager import WorkerManager
from novaclient.client import Client
from netifaces import interfaces, ifaddresses, AF_INET
import paramiko


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
        servers_to_init = []
        servers_to_start = []
        for i in range(0, num):
            server = self.nc.servers.create("G14Worker" + str(i), image, flavor, key_name="G14Key")
            servers_to_init.append(server)
        # loop as long as there are still servers to init/start
        while len(servers_to_init) > 0 or len(servers_to_start) > 0:
            still_to_init = []
            still_to_start = []
            for server in servers_to_init:
                if server.status == "BUILD":
                    still_to_init.append(self.nc.servers.get(server))
                else:
                    # get ip and associate it with server
                    print "A Server finished Build. Status: {0}".format(str(server.status))
                    ip = None
                    for key, network in server.networks.iteritems():
                        ip = network[0]
                        break
                    servers_to_start.append({"server": server, "ip": ip})
            for server in servers_to_start:
                # perform some operations via ssh on worker
                init_successful = self._init_worker(server["ip"])
                if not init_successful:
                    # init could not be performed
                    still_to_start.append(server)
                else:
                    # worker fully initialized
                    self._workers.append(server["server"])
            servers_to_init = still_to_init
            servers_to_start = still_to_start

    @staticmethod
    def _init_worker(workerip):
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(workerip), username="ubuntu")
            session = ssh.get_transport().open_session()
            session.exec_command(
                "cd airfoil-cloud-simulator/ && " +
                "screen -d -m celery worker -A workertasks -b amqp://cloudworker:worker@" +
                DefaultWorkerManager._my_ip() + "//")
            ssh.close()
            return True
        except:
            return False

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
