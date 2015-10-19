

class ComputeParameters:
    """
        Class holding the parameters for the computation using the airfoil binary.
    """
    def __init__(self):
        """
        Initialize instance variables (eventually with default values).
        :return: void
        """
        self.num_samples = None
        self.viscosity = None
        self.speed = None
        self.time = None
        self.xml_file = None
