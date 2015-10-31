from Storage import Storage
from utils import DBUtil
import json


class DatabaseStorage(Storage):

    def __init__(self, db_name):
        Storage.__init__(self)
        self._db_name = db_name
        DBUtil.execute_command(db_name, "CREATE TABLE IF NOT EXISTS Results (name TEXT PRIMARY KEY, value BLOB, started DATETIME, runtime FLOAT)")

    def save_result(self, model_params, compute_params, result, started=None, runtime=None):
        """
        This method stores the result identified by the parameters to the storage.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :param result: computation result
        :return: boolean, true if save was successful
        """
        hash_key = self.generate_hash(model_params, compute_params)
        self.save_result_hash(hash_key, json.dumps(result), started, runtime)
        return True

    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        hash_key = self.generate_hash(model_params, compute_params)
        result = DBUtil.execute_command(self._db_name, "SELECT value FROM Results WHERE name = (?)", (hash_key,), "ONE")
        print result
        return result is not None and result[0] != 'null'

    def get_result(self, model_params, compute_params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :rtype model.ComputeResult.ComputeResult|None
        """
        hash_key = self.generate_hash(model_params, compute_params)
        result = DBUtil.execute_command(self._db_name,
                                        "SELECT value, runtime, started FROM Results WHERE name = (?)",
                                        (hash_key,), "ONE")
        print "result: " + str(result[0])
        print "runtime: " + str(result[1])
        print "started: " + str(result[2])
        return result

    def save_result_hash(self, hash_key, result, started=None, endtime=None):
        precheck_result = DBUtil.execute_command(self._db_name,
                                                 "SELECT started FROM Results WHERE name = (?)", (hash_key,), "ONE")
        if precheck_result is not None:
            if started is not None:
                DBUtil.execute_command("UPDATE Results SET started = ? WHERE name = ?", (started,hash_key))
            if endtime is not None:
                runtime = endtime - precheck_result[0]
                print "RUNTIME: " + str(runtime)
                print "HASHKEY: " + str(hash_key)
                DBUtil.execute_command("UPDATE Results SET runtime = ? WHERE name = ?", (str(runtime), str(hash_key)))
            print "result already in database"
            return True
        if endtime is not None and started is not None:
            runtime = endtime - started
        else:
            runtime = None
        DBUtil.execute_command(self._db_name, "INSERT INTO Results(name, value, started, runtime) VALUES (?,?,?,?)",
                               (hash_key, result, started, runtime))
        return True


