from config import *
import sphere
import plane
import camera

class Scene:
    def __init__(self):
        self.spheres = [
            sphere.Sphere(
                center = [
                    np.random.uniform(low = 3.0, high = 10.0),
                    np.random.uniform(low = -5.0, high = 5.0),
                    np.random.uniform(low = -5.0, high = 5.0)
                ],
                radius = np.random.uniform(low = 0.1, high = 2.0),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ]
            ) for i in range(32)
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
            ),
            # plane.Plane(
            #     normal = [0, 0, -1],
            #     tangent= [1, 0, 0],
            #     bitangent= [0, 1, 0],
            #     uMin = -20,
            #     uMax = 20,
            #     vMin = -20,
            #     vMax = 20,
            #     center = [0, 0, 20],
            #     color = [
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0)
            #     ]
            # ),
            # plane.Plane(
            #     normal = [0, 1, 0],
            #     tangent= [1, 0, 0],
            #     bitangent= [0, 0, 1],
            #     uMin = -20,
            #     uMax = 20,
            #     vMin = -20,
            #     vMax = 20,
            #     center = [0, -20, 0],
            #     color = [
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0)
            #     ]
            # ),
            # plane.Plane(
            #     normal = [0, -1, 0],
            #     tangent= [0, 0, 1],
            #     bitangent= [1, 0, 0],
            #     uMin = -20,
            #     uMax = 20,
            #     vMin = -20,
            #     vMax = 20,
            #     center = [0, 20, 0],
            #     color = [
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0)
            #     ]
            # ),
            # plane.Plane(
            #     normal = [1, 0, 0],
            #     tangent= [0, 0, 1],
            #     bitangent= [0, 1, 0],
            #     uMin = -20,
            #     uMax = 20,
            #     vMin = -20,
            #     vMax = 20,
            #     center = [-20, 0, 0],
            #     color = [
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0)
            #     ]
            # ),
            # plane.Plane(
            #     normal = [-1, 0, 0],
            #     tangent= [0, 0, 1],
            #     bitangent= [0, 1, 0],
            #     uMin = -20,
            #     uMax = 20,
            #     vMin = -20,
            #     vMax = 20,
            #     center = [20, 0, 0],
            #     color = [
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0),
            #         np.random.uniform(low = 0.3, high = 1.0)
            #     ]
            # ),
        ]

        self.outDated = True