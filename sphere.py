from config import *

class Sphere:
    def __init__(self, center, radius, color, prop):
        self.center = np.array(center, dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
        self.prop = prop #0 reflect 1  no reflect