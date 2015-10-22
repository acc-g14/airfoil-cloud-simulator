from celery import Celery

from worker.compute.AirfoilComputation import AirfoilComputation
from worker.convert.GmshDolfinConverter import GmshDolfinConverter
from worker.create.GmshModelCreator import GmshModelCreator
from model.ModelParameters import ModelParameters
from model.ComputeParameters import ComputeParameters
import os

app = Celery("CloudProjectWorker", backend="amqp://", broker="amqp://")

creator = GmshModelCreator()
converter = GmshDolfinConverter()
computation = AirfoilComputation()


@app.task()
def simulate_airfoil(modelParams, computeParams):
    """
    :param model.ModelParameters.ModelParameters modelParams: ModelParameters
    :param model.ComputeParameters.ComputeParameters computeParams: ComputeParameters
    """
    root_dir = os.getcwd()
    working_dir = root_dir + "/workdir/" + str(modelParams.job) + "/a" + str(modelParams.angle)
    if not os.path.exists(working_dir): os.makedirs(working_dir)
    os.chdir(working_dir)

    msh_file = creator.create_model(modelParams)
    xml_file = converter.convert(msh_file)
    result = computation.perform_computation(computeParams, xml_file)
    result['angle'] = modelParams.angle

    os.chdir(root_dir)

    return result
