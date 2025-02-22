from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class SceneManager:
    def __init__(self):
        # Initialisation des shaders et autres ressources
        self.program = self.init_shaders()
        check_gl_errors()

    def load_shader_source(self, filepath):
        with open(filepath, 'r') as file:
            return file.read()

    def init_shaders(self):
        # Chargement des sources des shaders à partir des fichiers
        vertex_shader_source = self.load_shader_source('slashed_project/assets/shaders/vertex_shader.glsl')
        fragment_shader_source = self.load_shader_source('slashed_project/assets/shaders/fragment_shader.glsl')

        # Compilation et liaison des shaders
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)
        check_shader_compile_errors(vertex_shader)

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)
        check_shader_compile_errors(fragment_shader)

        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        check_program_link_errors(program)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        return program

    def init_scene(self):
        # Recharger les shaders (et recréer d'autres objets si nécessaire)
        self.program = self.init_shaders()
        # Ici vous pouvez également initialiser vos buffers, textures, etc.


    def render_scene(self, screen_width, screen_height, camera):
        if not (self.program and glIsProgram(self.program)):
            print("⚠️ Shader program non valide après changement de résolution, rechargement...")
            self.init_scene()  # Recharge les shaders si besoin

        glUseProgram(self.program)


        check_gl_errors()

        projection = camera.get_projection_matrix(screen_width, screen_height)
        projection_loc = glGetUniformLocation(self.program, "projection")
        if projection_loc == -1:
            print("Failed to get uniform location for 'projection'")
        check_gl_errors()

        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
        check_gl_errors()

        # Rendu de la scène
        # ...

        glUseProgram(0)
        check_gl_errors()

def check_shader_compile_errors(shader):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        error = glGetShaderInfoLog(shader)
        print(f"Shader compile error: {error}")

def check_program_link_errors(program):
    result = glGetProgramiv(program, GL_LINK_STATUS)
    if not result:
        error = glGetProgramInfoLog(program)
        print(f"Program link error: {error}")

def check_gl_errors():
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL Error: {error}")