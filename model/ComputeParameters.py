

class ComputeParameters:
    """
        Class holding the parameters for the computation using the airfoil binary.
    """
    def __init__(self, num_samples=None, viscosity=None, speed=None, time=None, server_ip=None):
        """
        Initialize instance variables (eventually with default values).
        :return: void
        """
        self.num_samples = num_samples
        self.viscosity = viscosity
        self.speed = speed
        self.time = time
        self.server_ip = server_ip
