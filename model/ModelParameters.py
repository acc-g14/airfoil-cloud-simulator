
class ModelParameters:
    """
        Class holding the parameters for creating and converting models.
    """
    def __init__(self, naca4=None, job=None, angle=None, num_nodes=None, refinement_level=None):
        """
        Initialize instance variables (eventually with default values).
        :return: void
        """
        self.naca4 = naca4
        self.job = job
        self.angle = angle
        self.num_nodes = num_nodes
        self.refinement_level = refinement_level
