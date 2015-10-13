import abc


class WorkerManager:
    """
    This class handles the initialization and deletion of workers.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def set_workers_available(self, num):
        """
        This method tries to the set the available workers num;
        either by initializing or deleting workers.

        :param int num: Number of workers
        """
        pass

    @abc.abstractmethod
    def get_number_of_workers(self):
        """
        Returns the number of currently available workers.
        :rtype : int
        """
        pass

    @abc.abstractmethod
    def get_max_number_of_workers(self):
        """
        Returns the maximum number of available workers, either
        defined by the program or limited by the environment.

        :rtype : int
        """
        pass
