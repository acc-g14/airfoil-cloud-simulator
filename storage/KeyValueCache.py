from Storage import Storage
import hashlib
import sqlite3


class KeyValueCache(Storage):
    def __init__(self, db_name):
        Storage.__init__(self)
        self._db_name = db_name
        conn = self._get_connection()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Results (name text PRIMARY KEY, value text)")
        conn.commit()
        conn.close()

    def generate_hash(self, model_params, compute_params):
        """
        This method generates a hash out of the parameters, which
        should be unique for a specific set of parameters.

        :rtype : str
        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        """
        builder = hashlib.md5()
        builder.update(str(model_params.angle))
        builder.update("|")
        for value in model_params.naca4:
            builder.update(str(value))
        builder.update("|")
        builder.update(str(model_params.num_nodes))
        builder.update("|")
        builder.update(str(model_params.refinement_level))
        builder.update("|")
        builder.update(str(compute_params.speed))
        builder.update("|")
        builder.update(str(compute_params.time))
        builder.update("|")
        builder.update(str(compute_params.viscosity))
        builder.update("|")
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
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Results VALUES (?,?)", (hash_key, result))
        conn.commit()
        conn.close()
        return True

    def has_result(self, model_params, compute_params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param model.ModelParameters.ModelParameters model_params: ModelParameters
        :param model.ComputeParameters.ComputeParameters compute_params: ComputeParameters
        :return: bool true if an entry is found, false otherwise
        """
        hash_key = self.generate_hash(model_params, compute_params)
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
        hash_key = self.generate_hash(model_params, compute_params)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Results WHERE name = (?)", (hash_key,))
        result = cursor.fetchone()
        conn.close()
        return result

    def _get_connection(self):
        return sqlite3.connect(self._db_name)

