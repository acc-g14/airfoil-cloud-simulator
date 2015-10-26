from urllib import urlencode
from celery import Celery

from worker.compute.AirfoilComputation import AirfoilComputation
from worker.convert.GmshDolfinConverter import GmshDolfinConverter
from worker.create.GmshModelCreator import GmshModelCreator
from storage.Storage import Storage
from utils import generate_hash
from model.ModelParameters import ModelParameters
from model.ComputeParameters import ComputeParameters
import os
import pycurl
import json
from Crypto.Cipher import AES
from urllib import urlencode

app = Celery("CloudProjectWorker", backend="amqp://", broker="amqp://")

creator = GmshModelCreator()
converter = GmshDolfinConverter()
computation = AirfoilComputation()

try:
    with open("key.aes", "r") as f:
        key = f.read()

    with open("iv.txt", "r") as f:
        iv = f.read()
    crypt_obj = AES.new(key, AES.MODE_ECB, iv)
except IOError:
    pass



@app.task()
def simulate_airfoil(model_params, compute_params, encrypted_swift_config):
    """
    :param model.ModelParameters.ModelParameters model_params: ModelParameters
    :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
    :param dict swift_config: dict
    """
    root_dir = os.getcwd()
    # print crypt_obj.decrypt(encrypted_swift_config)
    working_dir = root_dir + "/workdir/" + str(model_params.job) + "/a" + str(model_params.angle)
    if not os.path.exists(working_dir): os.makedirs(working_dir)
    os.chdir(working_dir)

    msh_file = creator.create_model(model_params)
    xml_file = converter.convert(msh_file)
    result = computation.perform_computation(compute_params, xml_file)
    result['angle'] = model_params.angle

    os.chdir(root_dir)

    hash_key = generate_hash(model_params, compute_params)
    post_data = urlencode({"result": json.dumps(result)})

    print post_data

    url = compute_params.server_ip + ":5000/save_result/" + hash_key

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.POSTFIELDS, post_data)
    c.perform()
    
    return None
