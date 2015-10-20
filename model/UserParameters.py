

class UserParameters:
    """
        Class holding parameters submitted by the user.
    """

    def __init__(self):
        """
            initialize variables
        """
        self.naca4 = None
        self.minAngle = 0
        self.maxAngle = 90
        self.step = 1
        self.numNodes = None
        self.refinementLevel = None
        self.num_samples = None
        self.viscosity = None
        self.speed = None
        self.time = None
