import abc


class Storage:

    def __init__(self):
        pass

    @abc.abstractmethod
    def generate_hash(self, params):
        """
        This method generates a hash out of the parameters, which
        should be unique for a specific set of parameters.

        :param params: Parameters to generate hash for.
        """
        return

    @abc.abstractmethod
    def save_result(self, params, result):
        """
        This method stores the result identified by the parameters to the storage.

        :param params: parameters result is based on.
        :param result: computation result
        :return: boolean, true if save was successful
        """
        return

    @abc.abstractmethod
    def has_result(self, params):
        """
        This method returns whether for the set of parameters passed an entry is found.

        :param params: set of parameters passed
        :return: bool true if an entry is found, false otherwise
        """
        return

    @abc.abstractmethod
    def get_result(self, params):
        """
        Returns the result associated with the set of parameters, None otherwise.

        :param params: Set of parameters to find entry for.
        :return: result if found, None otherwise
        """
        return
