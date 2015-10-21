import abc
from uuid import UUID


class ComputeManager(object):

    """
    This class handles all tasks computation-specific, like starting or stopping a
    computation or get the result or status for a specific job.
    """

    def __init__(self, storage):
        """
        Init the manager with the given storage engine.
        :param Storage.Storage storage: storage.Storage.Storage
        :return: void
        """
        self._storage = storage
        pass

    @abc.abstractmethod
    def start_computation(self, user_params):
        """
        This method starts the computation with the defined parameters.

        :param model.UserParameters.UserParameters user_params: UserParameters
        :rtype : UUID
        """
        return

    @abc.abstractmethod
    def stop_computation(self, job):
        """
        This method starts a specific job, TODO: exception if job already
        finished or not found?

        :param str job: job to stop
        :return: bool
        """
        return

    @abc.abstractmethod
    def get_result(self, job):
        """
        This method retrieves the (eventually partial) result for a specific job
        as list. TODO: raise exception if job is not found?

        :param str job: job to get results for
        :return: ComputeResult
        """
        return

    @abc.abstractmethod
    def get_status(self, job):
        """
        This method retrieves the status information for a specific job.
        :param basestring job: Job to get status for
        :return: str
        """
        return

