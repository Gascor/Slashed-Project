from OpenGL.GL import *
from OpenGL.GLU import *

class Cube:
    def __init__(self, position):
        self.position = position
        self.texture = None
        self.color = [1.0, 1.0, 1.0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        # Front face
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, -0.5)
        # Left face
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1, 1); glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, -0.5)
        # Right face
        glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0, 1); glVertex3f(0.5, 0.5, -0.5)
        # Top face
        glTexCoord2f(0, 0); glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1, 0); glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)
        # Bottom face
        glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1, 1); glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0, 1); glVertex3f(-0.5, -0.5, 0.5)
        glEnd()
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)

class Sphere:
    def __init__(self, position):
        self.position = position
        self.texture = None
        self.color = [1.0, 1.0, 1.0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)
        glColor3f(*self.color)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, 1, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)

class Plane:
    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.texture = None
        self.color = [1.0, 1.0, 1.0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-self.size, 0, -self.size)
        glTexCoord2f(1, 0); glVertex3f(self.size, 0, -self.size)
        glTexCoord2f(1, 1); glVertex3f(self.size, 0, self.size)
        glTexCoord2f(0, 1); glVertex3f(-self.size, 0, self.size)
        glEnd()
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)

class Cylinder:
    def __init__(self, position, radius, height):
        self.position = position
        self.radius = radius
        self.height = height
        self.texture = None
        self.color = [1.0, 1.0, 1.0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)
        glColor3f(*self.color)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluCylinder(quad, self.radius, self.radius, self.height, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)

class Cone:
    def __init__(self, position, base, height):
        self.position = position
        self.base = base
        self.height = height
        self.texture = None
        self.color = [1.0, 1.0, 1.0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        glScalef(*self.scale)
        glColor3f(*self.color)
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluCylinder(quad, self.base, 0, self.height, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)