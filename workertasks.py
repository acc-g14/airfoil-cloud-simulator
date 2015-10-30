from celery import Celery

from worker.compute.AirfoilComputation import AirfoilComputation
from worker.convert.GmshDolfinConverter import GmshDolfinConverter
from worker.create.GmshModelCreator import GmshModelCreator
from utils import generate_hash
from model.ModelParameters import ModelParameters
from model.ComputeParameters import ComputeParameters
from storage.SwiftStorage import SwiftStorage

from Crypto.Cipher import AES
from urllib import urlencode

import os
import pycurl
import json
from model.Config import Config

config = Config()
app = Celery("CloudProjectWorker", backend=config.backend, broker=config.broker)

creator = GmshModelCreator()
converter = GmshDolfinConverter()
computation = AirfoilComputation()

try:
    with open("key.aes", "r") as f:
        key = f.read()

    with open("iv.txt", "r") as f:
        iv = f.read()
    crypt_obj = AES.new(key.strip(), AES.MODE_ECB, iv.strip())
except IOError:
    pass



@app.task()
def simulate_airfoil(model_params, compute_params, encrypted_swift_config, container):
    """
    :param model.ModelParameters.ModelParameters model_params: ModelParameters
    :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
    :param dict swift_config: dict
    """

    #check if results are already in the objectstore
    swift_config = json.loads(crypt_obj.decrypt(encrypted_swift_config))
    swift = SwiftStorage(swift_config, container)

    if swift.has_result(model_params, compute_params):
        return swift.get_result(model_params, compute_params)

    #create a working directory for each task, this is to
    #avoid collisions between workers when they execute the airfoil binary
    root_dir = os.getcwd()
    working_dir = root_dir + "/workdir/" + str(model_params.job) + "/a" + str(model_params.angle)
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    os.chdir(working_dir)

    msh_file = creator.create_model(model_params)
    xml_file = converter.convert(msh_file)
    result = computation.perform_computation(compute_params, xml_file)
    result['angle'] = model_params.angle

    #reset working directory
    os.chdir(root_dir)

    #put result into object store, with the results hash_key as name
    swift.save_result(model_params, compute_params, result)

    return json.dumps(result)
