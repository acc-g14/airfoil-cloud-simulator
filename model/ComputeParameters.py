

class ComputeParameters:
    """
        Class holding the parameters for the computation.
    """
    def __init__(self):
        """
        Initialize instance variables (eventually with default values).
        :return: void
        """
        self.naca4 = None
        self.job = None
        self.angle = None
        self.num_nodes = None
        self.refinement_level = None
        self.navier_num_samples = None
        self.navier_viscosity = None
        self.navier_speed = None
        self.navier_time = None
