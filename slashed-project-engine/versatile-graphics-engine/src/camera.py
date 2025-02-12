import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, position, look_at):
        self.position = np.array(position, dtype=float)
        self.look_at = np.array(look_at, dtype=float)
        self.up = np.array([0, 1, 0], dtype=float)
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 0.1
        self.sensitivity = 0.1

    def set_view(self):
        direction = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ])
        self.look_at = self.position + direction
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.up[0], self.up[1], self.up[2]
        )

    def move_forward(self):
        direction = self.look_at - self.position
        direction = direction / np.linalg.norm(direction)
        self.position += direction * self.speed

    def move_backward(self):
        direction = self.look_at - self.position
        direction = direction / np.linalg.norm(direction)
        self.position -= direction * self.speed

    def move_left(self):
        direction = self.look_at - self.position
        direction = direction / np.linalg.norm(direction)
        right = np.cross(direction, self.up)
        right = right / np.linalg.norm(right)
        self.position -= right * self.speed

    def move_right(self):
        direction = self.look_at - self.position
        direction = direction / np.linalg.norm(direction)
        right = np.cross(direction, self.up)
        right = right / np.linalg.norm(right)
        self.position += right * self.speed

    def rotate(self, xoffset, yoffset):
        self.yaw += xoffset * self.sensitivity
        self.pitch += yoffset * self.sensitivity
        self.pitch = max(-89.0, min(89.0, self.pitch))