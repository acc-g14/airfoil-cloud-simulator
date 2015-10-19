import abc


class Computation:
    """
        Interface which is responsible for the computation at the worker.
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def perform_computation(self, params, file_name):
        """
        Actual method which performs the computation.
        :param model.ComputeParameters.ComputeParameters params: ComputeParameters
        :param string file_name
        :return: model.ComputeResult.ComputeResult
        """
        return
