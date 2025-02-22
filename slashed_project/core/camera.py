import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, position, target, up):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_sensitivity = 0.1

    def calculate_view_matrix(self):
        # Calculer la matrice de vue
        glLoadIdentity()
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )
        view_matrix = np.zeros((4, 4), dtype=np.float32)
        glGetFloatv(GL_MODELVIEW_MATRIX, view_matrix)
        return view_matrix

    def get_projection_matrix(self, screen_width, screen_height):
        # Calculer la matrice de projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, screen_width / screen_height, 0.1, 50.0)
        projection_matrix = np.zeros((4, 4), dtype=np.float32)
        glGetFloatv(GL_PROJECTION_MATRIX, projection_matrix)
        glMatrixMode(GL_MODELVIEW)
        return projection_matrix

    def move(self, direction, amount):
        if direction == "forward":
            self.position[2] -= amount
        elif direction == "backward":
            self.position[2] += amount
        elif direction == "left":
            self.position[0] -= amount
        elif direction == "right":
            self.position[0] += amount
        self.view_matrix = self.calculate_view_matrix()

    def rotate(self, x_offset, y_offset):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.position[0] += x_offset
        self.position[1] -= y_offset
        self.view_matrix = self.calculate_view_matrix()