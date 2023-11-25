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

        sphereData = []

        #allocate space - pass sphere data as 2 byte buffer
        #1st byte = (x, y, z, radius)
        #2nd byte = (r, g, b, _)
        self.sphereData = np.zeros(1024 * 8, dtype=np.float32)

        self.sphereDataBuffer = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.sphereDataBuffer)
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.sphereData.nbytes, self.sphereData, GL_DYNAMIC_READ)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.sphereDataBuffer)

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
        self.sphereData[8 * i] = _sphere.center[0] #x coord
        self.sphereData[8 * i + 1] = _sphere.center[1] #y coord
        self.sphereData[8 * i + 2] = _sphere.center[2] #z coord

        self.sphereData[8 * i + 3] = _sphere.radius

        self.sphereData[8 * i + 4] = _sphere.color[0] #r
        self.sphereData[8 * i + 5] = _sphere.color[1] #g
        self.sphereData[8 * i + 6] = _sphere.color[2] #b
    
    def prepareScene(self, scene):
        glUseProgram(self.rayTracerShader)

        #Pass camera params to program
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.position"), 1, scene.camera.position)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.forwards"), 1, scene.camera.forwards)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.right"), 1, scene.camera.right)
        glUniform3fv(glGetUniformLocation(self.rayTracerShader, "viewer.up"), 1, scene.camera.up)

        #Pass number of spheres to program
        glUniform1f(glGetUniformLocation(self.rayTracerShader, "sphereCount"), len(scene.spheres))

        #Pass spheres with params
        for i, _sphere in enumerate(scene.spheres):
            self.recordSphere(i, _sphere)

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.sphereDataBuffer)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, 8 * 4 * len(scene.spheres), self.sphereData)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.sphereDataBuffer)

    
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

