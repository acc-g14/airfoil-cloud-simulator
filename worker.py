from celery import Celery

from worker.compute.AirfoilComputation import AirfoilComputation
from worker.convert.GmshDolfinConverter import GmshDolfinConverter
from worker.create.GmshModelCreator import GmshModelCreator

app = Celery()

creator = GmshModelCreator()
converter = GmshDolfinConverter()
computation = AirfoilComputation()


@app.task()
def simulate_airfoil(modelParams, computeParams):
    """
    :param model.ComputeParameters.ComputeParameters params: ComputeParameters
    """
    msh_file = creator.create_model(modelParams)
    xml_file = converter.convert(modelParams.output_filename)
    result = computation.perform_computation(computeParams, xml_file)
    
    return result
