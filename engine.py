from config import *

class Engine:
    def __init__(self, width, height):
        self.screenWidth = width
        self.screenHeight = height

        #init opengl config
        self.shader = self.createShader("shaders/frameBufferVertex.glsl",
                                        "shaders/frameBufferFragment.glsl")
        
        self.rayTracerShader = self.createComputeShader("shaders/rayTracer.glsl")

        glUseProgram(self.shader)

        self.createQuad()
        self.createColorBuffer()
        self.createResourceMemory()

    def createQuad(self):
        #x, y, z, s, t
        self.vertices = np.array(
            ( 1.0, 1.0, 0.0, 1.0, 1.0,
              -1.0, 1.0, 0.0, 0.0, 1.0,
              -1.0, -1.0, 0.0, 0.0, 0.0,
              -1.0, -1.0, 0.0, 0.0, 0.0,
              1.0, -1.0, 0.0, 1.0, 0.0,
              1.0, 1.0, 0.0, 1.0, 1.0,),
              dtype=np.float32
        )

        self.vertex_count = 6

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def createColorBuffer(self):
        self.colorBuffer = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.colorBuffer)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, self.screenWidth, self.screenHeight, 0, GL_RGBA, GL_FLOAT, None)

    def createResourceMemory(self):
        #center := x, y, z
        #radius := radius
        #color := r, g, b
        #=> (x, y, z, radius), (r, g, b, _)

        # sphereData = []

        #allocate space - pass sphere data as 2 byte buffer
        #1st byte = (x, y, z, radius)
        #2nd byte = (r, g, b, _)

        #sphere := (x, y, z, radius) (r, g, b, _) (_, _, _, _) (_, _, _, _) (_, _, _, _)
        #plane  := (x, y, z, tx) (ty, tz, bx, by) (bz, nx, ny, nz) (umin, umax, vmin, vmax) (r, g, b, _)
        # for i in range(1024):
        #     for attribute in range(20):
        #         sphereData.append(0.0)

        objectData = np.zeros(1024*8, dtype=np.float32)

        self.objectData = np.array(objectData, dtype=np.float32)

        self.objectDataTexture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.objectDataTexture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 5, 1024, 0, GL_RGBA, GL_FLOAT, bytes(self.objectData))

    def createShader(self, vertexFilepath, framentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
        
        with open(framentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader
    
    def createComputeShader(self, filepath):
        with open(filepath, 'r') as f:
            compute_src = f.readlines()

        shader = compileProgram(compileShader(compute_src, GL_COMPUTE_SHADER))

        return shader
    
    def recordSphere(self, i, _sphere):
        #sphere := (x, y, z, radius) (r, g, b, _) (_, _, _, _) (_, _, _, _) (_, _, _, _)

        self.objectData[20 * i] = _sphere.center[0] #x coord
        self.objectData[20 * i + 1] = _sphere.center[1] #y coord
        self.objectData[20 * i + 2] = _sphere.center[2] #z coord

        self.objectData[20 * i + 3] = _sphere.radius

        self.objectData[20 * i + 4] = _sphere.color[0] #r
        self.objectData[20 * i + 5] = _sphere.color[1] #g
        self.objectData[20 * i + 6] = _sphere.color[2] #b

    def recordPlane(self, i, _plane):
        #plane  := (x, y, z, tx) (ty, tz, bx, by) (bz, nx, ny, nz) (umin, umax, vmin, vmax) (r, g, b, _)
        
        self.objectData[20 * i] = _plane.center[0] #x coord
        self.objectData[20 * i + 1] = _plane.center[1] #y coord
        self.objectData[20 * i + 2] = _plane.center[2] #z cord

        self.objectData[20 * i + 3] = _plane.tangent[0] #x tang
        self.objectData[20 * i + 4] = _plane.tangent[1] #y tang
        self.objectData[20 * i + 5] = _plane.tangent[2] #z tang

        self.objectData[20 * i + 6] = _plane.bitangent[0] #x bitang
        self.objectData[20 * i + 7] = _plane.bitangent[1] #y bitang
        self.objectData[20 * i + 8] = _plane.bitangent[2] #z bitang

        self.objectData[20 * i + 9] = _plane.normal[0] #x normal
        self.objectData[20 * i + 10] = _plane.normal[1] #y normal
        self.objectData[20 * i + 11] = _plane.normal[2] #z normal

        self.objectData[20 * i + 12] = _plane.uMin 
        self.objectData[20 * i + 13] = _plane.uMax
        self.objectData[20 * i + 14] = _plane.vMin
        self.objectData[20 * i + 15] = _plane.vMax 

        self.objectData[20 * i + 16] = _plane.color[0] #r
        self.objectData[20 * i + 17] = _plane.color[1] #g
        self.objectData[20 * i + 18] = _plane.color[2] #b 
    
    def updateScene(self, scene):
        scene.outDated = False
        glUseProgram(self.rayTracerShader)

        #Pass number of spheres to program
        glUniform1f(glGetUniformLocation(self.rayTracerShader, "sphereCount"), len(scene.spheres))

        #Pass spheres with params
        for i, _sphere in enumerate(scene.spheres):
            self.recordSphere(i, _sphere)

        #Pass number of planes to program
        glUniform1f(glGetUniformLocation(self.rayTracerShader, "planeCount"), len(scene.planes))
        sphereOffset = len(scene.spheres)
        #Pass planes with params
        for i, _plane in enumerate(scene.planes):
            self.recordPlane(i + sphereOffset, _plane)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.objectDataTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, 5, 1024, 0, GL_RGBA, GL_FLOAT, bytes(self.objectData))
        
        

    def prepareScene(self, scene):
        glUseProgram(self.rayTracerShader)

        #Pass camera params to program
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.position"), 1, scene.camera.position)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.forwards"), 1, scene.camera.forwards)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.right"), 1, scene.camera.right)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.up"), 1, scene.camera.up)

        if scene.outDated:
            self.updateScene(scene)

        glActiveTexture(GL_TEXTURE1)
        glBindImageTexture(1, self.objectDataTexture, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)

    
    def renderScene(self, scene):
        glUseProgram(self.rayTracerShader)

        self.prepareScene(scene)

        glActiveTexture(GL_TEXTURE0)
        glBindImageTexture(0, self.colorBuffer, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)

        glDispatchCompute(int(self.screenWidth/8), int(self.screenHeight/8), 1)

        #assert writing to image is done before read
        glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)
        glBindImageTexture(0, 0, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)
        self.drawScreen()

    def drawScreen(self):
        glUseProgram(self.shader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.colorBuffer)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        pg.display.flip()

    def destroy(self):
        glUseProgram(self.rayTracerShader)
        glMemoryBarrier(GL_ALL_BARRIER_BITS)
        glDeleteProgram(self.rayTracerShader)
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

