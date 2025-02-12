from OpenGL.GL import *
from OpenGL.GLUT import *

class Button:
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text

    def render(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.size[0], 0)
        glVertex2f(self.size[0], self.size[1])
        glVertex2f(0, self.size[1])
        glEnd()
        glPopMatrix()
        self.render_text()

    def render_text(self):
        glWindowPos2f(self.position[0] + 10, self.position[1] + 10)
        for ch in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

class Label:
    def __init__(self, position, text):
        self.position = position
        self.text = text

    def render(self):
        glWindowPos2f(self.position[0], self.position[1])
        for ch in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))