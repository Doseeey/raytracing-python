from config import *
import sphere
import camera

class Scene:
    def __init__(self):
        self.spheres = [
            sphere.Sphere(
                center = [
                    np.random.uniform(low = 3.0, high = 100.0),
                    np.random.uniform(low = -50.0, high = 50.0),
                    np.random.uniform(low = -50.0, high = 50.0)
                ],
                radius = np.random.uniform(low = 0.9, high = 5.0),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ]
            ) for i in range(256)
        ]

        self.camera = camera.Camera(
            position= [0, 0, 0]
        )