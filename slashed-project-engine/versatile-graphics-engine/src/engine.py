from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

class Engine:
    def __init__(self, camera):
        self.camera = camera
        self.objects = []
        self.models = []
        self.textures = {}

    def add_object(self, obj):
        self.objects.append(obj)

    def add_model(self, model):
        self.models.append(model)

    def set_texture(self, obj, texture):
        self.textures[obj] = texture

    def render(self):
        for obj in self.objects:
            if obj in self.textures:
                glBindTexture(GL_TEXTURE_2D, self.textures[obj])
            else:
                print(f"⚠️ L'objet {obj} n'a pas de texture assignée !")
            obj.render()
        for model in self.models:
            model.render()

    def update(self, delta_time):
        for model in self.models:
            model.update(delta_time)