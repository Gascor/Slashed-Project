from OpenGL.GL import *
from OpenGL.GLU import *
from objects import Plane

class Map:
    def __init__(self, size):
        self.size = size
        self.ground = Plane(position=[0, -1, 0], size=size)

    def render(self):
        self.ground.render()