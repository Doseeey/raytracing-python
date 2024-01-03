from config import *
import engine
import scene

class App:
    def __init__(self):
        pg.init()
        self.screenWidth = 800
        self.screenHeight = 600
        #OpenGL 4.3 needed for computeShaders()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        
        pg.display.set_mode((self.screenWidth, self.screenHeight), pg.OPENGL|pg.DOUBLEBUF)
        self.graphicsEngine = engine.Engine(self.screenWidth, self.screenHeight)
        self.scene = scene.Scene()

        self.lastTime = pg.time.get_ticks()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        self.lightCount = 0

        self.mainLoop()

    def mainLoop(self):
        running = True
        while (running):

            #Events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                if (event.type == pg.KEYDOWN):
                    if (event.key == pg.K_ESCAPE):
                        running == False

            #Camera movement
            travelSpeed = 0.1
            rotateSpeed = 1
            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.scene.camera.position[0] += travelSpeed
            if keys[pg.K_s]:
                self.scene.camera.position[0] -= travelSpeed
            if keys[pg.K_a]:
                self.scene.camera.position[1] += travelSpeed
            if keys[pg.K_d]:
                self.scene.camera.position[1] -= travelSpeed
            if keys[pg.K_SPACE]:
                self.scene.camera.position[2] += travelSpeed
            if keys[pg.K_LSHIFT]:
                self.scene.camera.position[2] -= travelSpeed
            if keys[pg.K_UP]:
                self.scene.camera.updateVectors(self.scene.camera.theta, self.scene.camera.phi+rotateSpeed)
            if keys[pg.K_DOWN]:
                self.scene.camera.updateVectors(self.scene.camera.theta, self.scene.camera.phi-rotateSpeed)
            if keys[pg.K_LEFT]:
                self.scene.camera.updateVectors(self.scene.camera.theta+rotateSpeed, self.scene.camera.phi)
            if keys[pg.K_RIGHT]:
                self.scene.camera.updateVectors(self.scene.camera.theta-rotateSpeed, self.scene.camera.phi)
            #Render
            self.graphicsEngine.renderScene(self.scene)

            #Timing
            self.calculateFramerate()

        self.quit()

    def calculateFramerate(self):
        self.currentTime = pg.time.get_ticks()
        delta = self.currentTime - self.lastTime

        if (delta >= 1000):
            framerate = max(1, int(1000.0 * self.numFrames/delta))
            pg.display.set_caption(f"{framerate} fps")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = float(1000.0 / max(1, framerate))
        
        self.numFrames += 1

    def quit(self):
        pg.quit()

