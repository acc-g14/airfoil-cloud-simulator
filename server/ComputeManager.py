import abc
from uuid import UUID
from storage.Storage import Storage


class ComputeManager:

    """
    This class handles all tasks computation-specific, like starting or stopping a
    computation or get the result or status for a specific job.
    """

    def __init__(self, storage):
        """
        Init the manager with the given storage engine.
        :param Storage storage: Storage
        :return: void
        """
        self._storage = storage
        pass

    @abc.abstractmethod
    def start_computation(self, params):
        """
        This method starts the computation with the defined parameters.

        :param params: ComputeParameters
        :rtype : UUID
        """
        return

    @abc.abstractmethod
    def stop_computation(self, job):
        """
        This method starts a specific job, TODO: exception if job already
        finished or not found?

        :param UUID job: Job to stop
        :return: boolean, true if job has been successfully stopped.
        """
        return

    @abc.abstractmethod
    def get_result(self, job):
        """
        This method retrieves the (eventually partial) result for a specific job
        as list. TODO: raise exception if job is not found?

        :param basestring job: Job to get result for
        :return: TODO
        """
        return

    @abc.abstractmethod
    def get_status(self, job):
        """
        This method retrieves the status information for a specific job.
        :param basestring job: Job to get status for
        :return: TODO
        """
        return

