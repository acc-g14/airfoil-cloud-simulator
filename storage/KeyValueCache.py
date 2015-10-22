from Storage import Storage
from utils import generate_hash
import sqlite3
import json


class KeyValueCache(Storage):

    def __init__(self, db_name):
        Storage.__init__(self)
        self._db_name = db_name
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Results (name text PRIMARY KEY, value blob)")
        conn.commit()
        conn.close()

    def save_result(self, model_params, compute_params, result):
        """
        This method stores the result identified by the parameters to the storage.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :param result: computation result
        :return: boolean, true if save was successful
        """
        hash_key = generate_hash(model_params, compute_params)
        self.save_result_hash(hash_key, json.dumps(result))
        return True

    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        hash_key = generate_hash(model_params, compute_params)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Results WHERE name = (?)", (hash_key,))
        result = cursor.fetchone()
        print result
        conn.close()
        return result is not None

    def get_result(self, model_params, compute_params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :rtype model.ComputeResult.ComputeResult|None
        """
        hash_key = generate_hash(model_params, compute_params)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM Results WHERE name = (?)", (hash_key,))
        result = cursor.fetchone()[0]
        print result
        conn.close()
        return json.loads(result)

    def save_result_hash(self, hash_key, result):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Results VALUES (?,?)", (hash_key, result))
        conn.commit()
        conn.close()
        return True

    def _get_connection(self):
        return sqlite3.connect(self._db_name)

