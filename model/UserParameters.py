

class UserParameters:
    """
        Class holding parameters submitted by the user.
    """

    def __init__(self):
        """
            initialize variables
        """
        self.naca4 = [0, 0, 1, 2]
        self.min_angle = 0
        self.max_angle = 90
        self.step = 10
        self.num_nodes = 200
        self.refinement_level = 0
        self.num_samples = 2
        self.viscosity = 0.0001
        self.speed = 10
        self.time = 0.1
