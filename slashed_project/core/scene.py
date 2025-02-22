from OpenGL.GL import *
import numpy as np
from utils.texture_loader import load_texture

class Scene:
    def __init__(self):
        self.objects = []
        self.lights = []

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, light):
        self.lights.append(light)

    def render(self, shader_program):
        glUseProgram(shader_program)
        
        # Configurer les lumières
        for i, light in enumerate(self.lights):
            light.setup(shader_program, i)
        
        # Rendre les objets
        for obj in self.objects:
            obj.render(shader_program)
        
        glUseProgram(0)

    def update(self, delta_time):
        for obj in self.objects:
            obj.update(delta_time)

class Cube:
    def __init__(self):
        self.vertices = np.array([
            -1, -1, -1,
             1, -1, -1,
             1,  1, -1,
            -1,  1, -1,
            -1, -1,  1,
             1, -1,  1,
             1,  1,  1,
            -1,  1,  1,
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            0, 1, 5, 5, 4, 0,
            2, 3, 7, 7, 6, 2,
            0, 3, 7, 7, 4, 0,
            1, 2, 6, 6, 5, 1,
        ], dtype=np.uint32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

    def render(self, shader_program):
        model = np.identity(4, dtype=np.float32)
        model = np.dot(model, self.translate(self.position))
        model = np.dot(model, self.rotate(self.rotation))
        model = np.dot(model, self.scale_matrix(self.scale))

        model_loc = glGetUniformLocation(shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def translate(self, position):
        translation = np.identity(4, dtype=np.float32)
        translation[3, :3] = position
        return translation

    def rotate(self, rotation):
        rx, ry, rz = np.radians(rotation)
        cosx, sinx = np.cos(rx), np.sin(rx)
        cosy, siny = np.cos(ry), np.sin(ry)
        cosz, sinz = np.cos(rz), np.sin(rz)

        rotx = np.array([
            [1, 0, 0, 0],
            [0, cosx, -sinx, 0],
            [0, sinx, cosx, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        roty = np.array([
            [cosy, 0, siny, 0],
            [0, 1, 0, 0],
            [-siny, 0, cosy, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        rotz = np.array([
            [cosz, -sinz, 0, 0],
            [sinz, cosz, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        return np.dot(np.dot(rotx, roty), rotz)

    def scale_matrix(self, scale):
        scaling = np.identity(4, dtype=np.float32)
        scaling[0, 0] = scale[0]
        scaling[1, 1] = scale[1]
        scaling[2, 2] = scale[2]
        return scaling

    def update(self, delta_time):
        # Mettre à jour les transformations ou autres propriétés si nécessaire
        pass

class Plane:
    def __init__(self, texture_path=None):
        self.vertices = np.array([
            -1, 0, -1,
             1, 0, -1,
             1, 0,  1,
            -1, 0,  1,
        ], dtype=np.float32)

        self.tex_coords = np.array([
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,
        ], dtype=np.uint32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.tbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, self.tbo)
        glBufferData(GL_ARRAY_BUFFER, self.tex_coords.nbytes, self.tex_coords, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 2 * self.tex_coords.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self.texture = load_texture(texture_path) if texture_path else None

        self.position = [0, 0, -5]
        self.rotation = [0, 0, 0]
        self.scale = [5, 5, 5]

    def render(self, shader_program):
        model = np.identity(4, dtype=np.float32)
        model = np.dot(model, self.translate(self.position))
        model = np.dot(model, self.rotate(self.rotation))
        model = np.dot(model, self.scale_matrix(self.scale))

        model_loc = glGetUniformLocation(shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)

        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        if self.texture:
            glBindTexture(GL_TEXTURE_2D, 0)

    def translate(self, position):
        translation = np.identity(4, dtype=np.float32)
        translation[3, :3] = position
        return translation

    def rotate(self, rotation):
        rx, ry, rz = np.radians(rotation)
        cosx, sinx = np.cos(rx), np.sin(rx)
        cosy, siny = np.cos(ry), np.sin(ry)
        cosz, sinz = np.cos(rz), np.sin(rz)

        rotx = np.array([
            [1, 0, 0, 0],
            [0, cosx, -sinx, 0],
            [0, sinx, cosx, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        roty = np.array([
            [cosy, 0, siny, 0],
            [0, 1, 0, 0],
            [-siny, 0, cosy, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        rotz = np.array([
            [cosz, -sinz, 0, 0],
            [sinz, cosz, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        return np.dot(np.dot(rotx, roty), rotz)

    def scale_matrix(self, scale):
        scaling = np.identity(4, dtype=np.float32)
        scaling[0, 0] = scale[0]
        scaling[1, 1] = scale[1]
        scaling[2, 2] = scale[2]
        return scaling

    def update(self, delta_time):
        # Mettre à jour les transformations ou autres propriétés si nécessaire
        pass