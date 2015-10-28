import abc
import utils


class Storage:

    def __init__(self):
        pass

    def generate_hash(self, model_params, compute_params):
        return utils.generate_hash(model_params, compute_params)

    @abc.abstractmethod
    def save_result_hash(self, hash_key, result):
        pass

    @abc.abstractmethod
    def save_result(self, model_params, compute_params, result):
        """
        This method stores the result identified by the parameters to the storage.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :param result: computation result
        :return: boolean, true if save was successful
        """
        return

    @abc.abstractmethod
    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        return

    @abc.abstractmethod
    def get_result(self, model_params, compute_params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: result if found, None otherwise
        """
        return
