from Storage import Storage
from utils import DBUtil
import json


class KeyValueCache(Storage):

    def __init__(self, db_name):
        Storage.__init__(self)
        self._db_name = db_name
        DBUtil.execute_command(db_name, "CREATE TABLE IF NOT EXISTS Results (name text PRIMARY KEY, value blob)")

    def save_result(self, model_params, compute_params, result):
        """
        This method stores the result identified by the parameters to the storage.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :param result: computation result
        :return: boolean, true if save was successful
        """
        hash_key = self.generate_hash(model_params, compute_params)
        self.save_result_hash(hash_key, json.dumps(result))
        return True

    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        hash_key = self.generate_hash(model_params, compute_params)
        result = DBUtil.execute_command(self._db_name, "SELECT * FROM Results WHERE name = (?)", (hash_key,), "ONE")
        print result
        return result is not None

    def get_result(self, model_params, compute_params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :rtype model.ComputeResult.ComputeResult|None
        """
        hash_key = self.generate_hash(model_params, compute_params)
        result = DBUtil.execute_command(self._db_name, "SELECT * FROM Results WHERE name = (?)", (hash_key,), "ONE")
        return json.loads(result[0])

    def save_result_hash(self, hash_key, result):
        DBUtil.execute_command(self._db_name, "INSERT INTO Results VALUES (?,?)", (hash_key, result))
        return True


