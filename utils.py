from netifaces import interfaces, ifaddresses, AF_INET
import hashlib

def find_server_by_ip(ip, nc):
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
    builder.update(str(model_params.angle))
    builder.update("|")
    for value in model_params.naca4:
        builder.update(str(value))
        builder.update("|")
        builder.update(str(model_params.num_nodes))
        builder.update("|")
        builder.update(str(model_params.refinement_level))
        builder.update("|")
        builder.update(str(compute_params.speed))
        builder.update("|")
        builder.update(str(compute_params.time))
        builder.update("|")
        builder.update(str(compute_params.viscosity))
        builder.update("|")
        builder.update(str(compute_params.num_samples))
        return builder.hexdigest()
