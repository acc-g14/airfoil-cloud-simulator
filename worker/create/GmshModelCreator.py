from worker.create.ModelCreator import ModelCreator


class GmshModelCreator(ModelCreator):
    """
        Class to create a gmsh model based on parameters.
    """
    def create_model(self, params):
        """
        Creates a gmsh model based on given parameters.
        :param model.ComputeParameters.ComputeParameters params: ComputeParameters
        :return: str - filename
        """
        pass