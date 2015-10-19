import abc


class ModelCreator:
    """
        Interface to create a model.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def create_model(self, params):
        """
        Method that creates a model based on the passed parameters
        :param model.ModelParameters.ModelParameters params: ModelParameters
        :return:
        """
        pass
