from config import *
import sphere
import plane
import camera

class Scene:
    def __init__(self):
        self.spheres = [
            sphere.Sphere(
                center = [
                    np.random.uniform(low = 3.0, high = 100.0),
                    np.random.uniform(low = -50.0, high = 50.0),
                    np.random.uniform(low = -5.0, high = 50.0)
                ],
                radius = np.random.uniform(low = 1.0, high = 5.0),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ],
                prop = np.random.randint(2)
            ) for i in range(128)
        ]

        self.camera = camera.Camera(
            position= [-5, 0, 0]
        )

        self.planes = [
            plane.Plane(
                normal = [0, 0, 1],
                tangent= [1, 0, 0],
                bitangent= [0, 1, 0],
                uMin = -200,
                uMax = 200,
                vMin = -200,
                vMax = 200,
                center = [0, 0, -20],
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ]
            )
        ]

        self.outDated = True