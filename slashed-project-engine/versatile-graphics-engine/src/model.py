from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront

class Model:
    def __init__(self, filepath):
        self.scene = pywavefront.Wavefront(filepath, collect_faces=True)

    def render(self):
        for name, mesh in self.scene.meshes.items():
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    vertex = self.scene.vertices[vertex_i]
                    glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()

    def update(self, delta_time):
        # Implement animation update logic if needed
        pass