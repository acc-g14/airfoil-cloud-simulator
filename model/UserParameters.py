

class UserParameters:
    """
        Class holding parameters submitted by the user.
    """

    def __init__(self):
        """
            initialize variables
        """
        self.naca4 = [0, 0, 1, 2]
        self.minAngle = 0
        self.maxAngle = 90
        self.step = 10
        self.numNodes = 200
        self.refinementLevel = 0
        self.num_samples = 2
        self.viscosity = 0.0001
        self.speed = 10
        self.time = 0.1
