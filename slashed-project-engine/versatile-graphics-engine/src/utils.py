from PIL import Image
import numpy as np
from OpenGL.GL import *

def load_texture(filepath):
    try:
        print(f"🔄 Chargement de la texture : {filepath}")
        image = Image.open(filepath)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        width, height = image.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glBindTexture(GL_TEXTURE_2D, 0)

        print(f"✅ Texture chargée avec ID : {texture_id}")
        return texture_id
    except Exception as e:
        print(f"❌ Erreur de chargement de la texture {filepath} : {e}")
        return None

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Index out of range for Vector3D")

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def add(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, factor):
        return Vector3D(self.x * factor, self.y * factor, self.z * factor)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector3D()
        return self.scale(1 / mag)