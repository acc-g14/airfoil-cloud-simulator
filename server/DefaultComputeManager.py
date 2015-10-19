from ComputeManager import ComputeManager


class DefaultComputeManager(ComputeManager):

    def __init__(self, storage):
        super(DefaultComputeManager, self).__init__(storage)

    def stop_computation(self, job):
        pass

    def get_status(self, job):
        pass

    def get_result(self, job):
        pass

    def start_computation(self, model_params, compute_params):
        """
        This method starts the computation with the defined parameters.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :rtype : UUID
        """
