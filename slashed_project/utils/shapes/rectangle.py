from OpenGL.GL import *

class Rectangle:
    def __init__(self, x, y, width, height, color=(0.2, 0.2, 0.2)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y + self.height)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x, self.y)
        glEnd()