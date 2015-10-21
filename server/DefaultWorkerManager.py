from WorkerManager import WorkerManager
from novaclient.client import Client
from netifaces import interfaces, ifaddresses, AF_INET
import paramiko
import os


class DefaultWorkerManager(WorkerManager):
    novaconfig = {'username': os.environ['OS_USERNAME'],
                  'api_key': os.environ['OS_PASSWORD'],
                  'project_id': os.environ['OS_TENANT_NAME'],
                  'auth_url': os.environ['OS_AUTH_URL'],
                  }
    nc = Client('2', **novaconfig)

    MAX_NUMBER = 10

    def __init__(self):
        WorkerManager.__init__(self)
        self._workers = []

    def get_max_number_of_workers(self):
        return DefaultWorkerManager.MAX_NUMBER

    def get_number_of_workers(self):
        return len(self._workers)

    def set_workers_available(self, num):
        self.start_workers(num)

    def start_workers(self, num):
        image = self.nc.images.find(name="MMProjectWorker")
        flavor = self.nc.flavors.find(name="m1.medium")
        servers_to_init = []
        servers_to_start = []
        for i in range(0, num):
            # TODO
            server = self.nc.servers.create("MMProjectWorker" + str(i), image, flavor, key_name="G14Key")
            servers_to_init.append(server)
        while len(servers_to_init) > 0 or len(servers_to_start) > 0:
            still_to_init = []
            still_to_start = []
            for server in servers_to_init:
                if server.status == "BUILD":
                    still_to_init.append(self.nc.servers.get(server))
                else:
                    print "Server finished Build. Status: {0}".format(str(server.status))
                    ip = None
                    for key, network in server.networks.iteritems():
                        ip = network[0]
                        break
                    print ip
                    servers_to_start.append({"server": server, "ip": ip})
            print len(servers_to_start)
            for server in servers_to_start:
                init_successful = self._init_worker(server["ip"])
                if not init_successful:
                    still_to_start.append(server)
                else:
                    self._workers.append(server["server"])
            servers_to_init = still_to_init
            servers_to_start = still_to_start
        pass

    @staticmethod
    def _init_worker(workerip):
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(str(workerip), username="ubuntu")
            session = ssh.get_transport().open_session()
            # TODO adapt call to register on server
            session.exec_command(
                "cd airfoil-cloud-simulator/ && " +
                "screen -d -m celery worker -A workertasks -b amqp://cloudworker:worker@" +
                DefaultWorkerManager.my_ip() + "//")
            ssh.close()
            return True

    # from http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    @staticmethod
    def my_ip():
        """
        :rtype : string
        """
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
            if ifaceName == "eth0":
                print "My IP:" + addresses[0]
                return addresses[0]

    @staticmethod
    def _shutdown_worker(self, worker):
        # TODO
        pass
