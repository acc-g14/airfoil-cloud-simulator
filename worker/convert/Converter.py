import abc


class Converter:
    """
        Interface to perform convertion.
    """

    def __init__(self):
        """
        Constructor method.
        :return: void
        """
        pass

    @abc.abstractmethod
    def convert(self, f):
        """
        Converts a given file.
        :param file f: file
        :return: file converted file
        """
        return
