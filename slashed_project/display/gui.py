from OpenGL.GL import *
from OpenGL.GLUT import *

class Dropdown:
    def __init__(self, label, x, y, width, height, options, callback):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.callback = callback
        self.selected_index = 0
        self.expanded = False

    def draw(self):
        # Dessiner le label
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(self.x, self.y + self.height + 10)
        for char in self.label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char)) # type: ignore

        # Dessiner la boîte déroulante
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # Dessiner l'option sélectionnée
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(self.x + 10, self.y + self.height / 2 - 5)
        for char in self.options[self.selected_index]:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char)) # type: ignore

        # Dessiner les options si la liste est déroulée
        if self.expanded:
            self.draw_options()

    def draw_options(self):
        # Dessiner le rectangle de fond pour les options
        glColor3f(0.1, 0.1, 0.1)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y - len(self.options) * self.height)
        glVertex2f(self.x + self.width, self.y - len(self.options) * self.height)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x, self.y)
        glEnd()

        for i, option in enumerate(self.options):
            y_offset = (i + 1) * self.height
            glColor3f(0.2, 0.2, 0.2)
            glBegin(GL_QUADS)
            glVertex2f(self.x, self.y - y_offset)
            glVertex2f(self.x + self.width, self.y - y_offset)
            glVertex2f(self.x + self.width, self.y - y_offset + self.height)
            glVertex2f(self.x, self.y - y_offset + self.height)
            glEnd()

            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(self.x + 10, self.y - y_offset + self.height / 2 - 5)
            for char in option:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char)) # type: ignore

    def handle_click(self, x, y):
        if self.expanded:
            for i, option in enumerate(self.options):
                y_offset = (i + 1) * self.height
                if self.x <= x <= self.x + self.width and self.y - y_offset <= y <= self.y - y_offset + self.height:
                    self.selected_index = i
                    self.expanded = False
                    self.callback(self.options[self.selected_index])
                    return True
            self.expanded = False
            return False
        elif self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.expanded = not self.expanded
            return True
        return False

    def close(self):
        self.expanded = False

    def adjust_size(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Button:
    def __init__(self, label, x, y, width, height, callback):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

    def draw(self):
        glColor3f(0.7, 0.7, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        glColor3f(0, 0, 0)
        glRasterPos2f(self.x + 10, self.y + 20)
        for char in self.label:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char)) # type: ignore


    def is_inside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def click(self):
        self.callback()

    def adjust_size(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height