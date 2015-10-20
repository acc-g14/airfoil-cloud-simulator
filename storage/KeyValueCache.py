from Storage import Storage
import hashlib


class KeyValueCache(Storage):
    def __init__(self):
        Storage.__init__(self)
        self._hashmap = {}

    def generate_hash(self, model_params, compute_params):
        """
        This method generates a hash out of the parameters, which
        should be unique for a specific set of parameters.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        """
        builder = hashlib.sha256()
        builder.update(str(model_params.angle))
        builder.update(str(model_params.naca4))
        builder.update(str(model_params.num_nodes))
        builder.update(str(model_params.refinement_level))
        builder.update(str(compute_params.speed))
        builder.update(str(compute_params.time))
        builder.update(str(compute_params.viscosity))
        builder.update(str(compute_params.num_samples))
        return builder.hexdigest()

    def save_result(self, model_params, compute_params, result):
        """
        This method stores the result identified by the parameters to the storage.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :param result: computation result
        :return: boolean, true if save was successful
        """
        hash_key = self.generate_hash(model_params, compute_params)
        self._hashmap[hash_key] = result
        return True

    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        hash_key = self.generate_hash(model_params, compute_params)
        return self._hashmap.has_key(hash_key)

    def get_result(self, model_params, compute_params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: result if found, None otherwise
        """
        hash_key = self.generate_hash(model_params, compute_params)
        return self._hashmap.get(hash_key) or None

