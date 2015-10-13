import abc


class Computation:
    """
        Interface which is responsible for the computation at the worker.
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def perform_computation(self, params):
        """
        Actual method which performs the computation.
        :param model.ComputeParameters.ComputeParameters params: ComputeParameters
        :return: model.ComputeResult.ComputeResult
        """
        return
