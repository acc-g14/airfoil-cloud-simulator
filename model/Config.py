import ConfigParser
from Crypto.Cipher import AES
from utils import id_generator
import os


class Config:

    def __init__(self):
        parser = ConfigParser.SafeConfigParser()
        parser.readfp(open("defaults.cfg"))
        self.swift_config = {'user': os.environ['OS_USERNAME'],
                             'key': os.environ['OS_PASSWORD'],
                             'tenant_name': os.environ['OS_TENANT_NAME'],
                             'authurl': os.environ['OS_AUTH_URL']}
        self.nova_config = {'username': os.environ['OS_USERNAME'],
                            'api_key': os.environ['OS_PASSWORD'],
                            'project_id': os.environ['OS_TENANT_NAME'],
                            'auth_url': os.environ['OS_AUTH_URL']}
        self.container = parser.get("swift", "container")
        self.max_workers = parser.getint("workers", "max")
        self.min_workers = parser.getint("workers", "min")
        self.worker_timeout = parser.getint("workers", "timeout")
        key_filename = parser.get("security", "key_file")
        iv_filename = parser.get("security", "iv_file")
        self.key = self._read_file(key_filename, 32)
        self.iv = self._read_file(iv_filename, 16)
        self.db_name = parser.get("server", "db_name")
        self.backend = parser.get("server", "backend")
        self.broker = parser.get("server", "broker")
        self.crypt_obj = AES.new(self.key, AES.MODE_ECB, self.iv)
        self.password = parser.get("server", "password")
        self.username = parser.get("server", "username")
        self.debug = parser.get("server", "debug")
        self.secret_key = parser.get("server", "secret_key")


    @staticmethod
    def _read_file(filename, length):
        try:
            with open(filename, "r") as myfile:
                return myfile.read().replace("\n", "")
        except IOError:
            with open(filename, "w") as f:
                key = id_generator(length)
                f.write(key)
                return key

