from config import *

class Plane:

    def __init__(self, normal, tangent, bitangent, uMin, uMax, vMin, vMax, center, color):

        self.normal = np.array(normal, dtype=np.float32)
        self.tangent = np.array(tangent, dtype=np.float32)
        self.bitangent = np.array(bitangent, dtype=np.float32)
        self.uMin = uMin
        self.uMax = uMax
        self.vMin = vMin
        self.vMax = vMax
        self.center = np.array(center, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        