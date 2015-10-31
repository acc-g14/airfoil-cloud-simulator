from netifaces import interfaces, ifaddresses, AF_INET
import hashlib
import string
import random
import sqlite3


def find_vm_by_ip(ip, nc):
    """
    Finds a virtual machine given an ip
    """
    for s in nc.servers.list():
        if s.networks.has_key("ACC-Course-net"):
            print s.networks["ACC-Course-net"]
            if ip in s.networks["ACC-Course-net"]: return s
    return None


def server_ip():
    """
    :rtype : string
    """
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        if ifaceName == "eth0":
            return addresses[0]


def generate_hash(model_params, compute_params):
    """
    This method generates a hash out of the parameters, which
    should be unique for a specific set of parameters.
    
    :rtype : str
    :param model.ModelParameters.ModelParameters model_params: ModelParameters
    :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
    """
    builder = hashlib.md5()
    builder.update(str(float(model_params.angle)))
    builder.update("|")
    for value in model_params.naca4:
        builder.update(str(float(value)))
        builder.update("|")
    builder.update(str(model_params.num_nodes))
    builder.update("|")
    builder.update(str(model_params.refinement_level))
    builder.update("|")
    builder.update(str(float(compute_params.speed)))
    builder.update("|")
    builder.update(str(float(compute_params.time)))
    builder.update("|")
    builder.update(str(float(compute_params.viscosity)))
    return builder.hexdigest()


def id_generator(size, chars=string.ascii_uppercase + string.digits):
    """
    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    return ''.join(random.choice(chars) for _ in range(size))

class DBUtil:

    @classmethod
    def execute_command(cls, db_name, command, params=None, fetch=None):
        conn = sqlite3.connect(db_name)
        conn.execute("PRAGMA busy_timeout = 30000")
        c = conn.cursor()
        if params is None:
            c.execute(command)
        else:
            c.execute(command, params)
        if fetch == "ALL":
            result = c.fetchall()
        elif fetch == "ONE":
            result = c.fetchone()
        elif isinstance(fetch, int):
            result = c.fetchmany(fetch)
        else:
            result = None
        conn.commit()
        conn.close()
        return result