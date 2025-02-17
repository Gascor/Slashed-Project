from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class GameEngine:
    def __init__(self, screen_width, screen_height, fullscreen=True):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fullscreen = fullscreen

    def init_window(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.screen_width, self.screen_height)
        glutCreateWindow(b'Slashed Project')
        if self.fullscreen:
            glutFullScreen()

    def init_opengl(self):
        glEnable(GL_DEPTH_TEST)
        self.check_gl_errors()

    def check_gl_errors(self):
        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL Error: {error}")

    def run(self):
        glutMainLoop()