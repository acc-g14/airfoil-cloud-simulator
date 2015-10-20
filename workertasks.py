from celery import Celery

from worker.compute.AirfoilComputation import AirfoilComputation
from worker.convert.GmshDolfinConverter import GmshDolfinConverter
from worker.create.GmshModelCreator import GmshModelCreator
from model.ModelParameters import ModelParameters
from model.ComputeParameters import ComputeParameters

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
    msh_file = creator.create_model(modelParams)
    xml_file = converter.convert(msh_file)
    result = computation.perform_computation(computeParams, xml_file)
    result['angle'] = modelParams.angle
    return result
