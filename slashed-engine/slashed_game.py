from core.game_engine import GameEngine
from core.scene_manager import SceneManager
from display.menu_manager import MenuManager
from core.camera import Camera
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import threading

class SlashedGame(GameEngine):
    def __init__(self, screen_width, screen_height, fullscreen=True):
        super().__init__(screen_width, screen_height, fullscreen)
        self.scene_manager = None
        self.menu_manager = MenuManager(self)
        self.camera = Camera(position=[0, 0, 5], target=[0, 0, 0], up=[0, 1, 0])
        self.mouse_left_pressed = False
        self.cinematic = None
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = screen_width
        self.viewport_height = screen_height

    def init(self):
        self.init_window()
        self.init_opengl()
        self.scene_manager = SceneManager()  # Initialiser SceneManager après l'initialisation OpenGL
        self.scene_manager.init_scene()
        self.check_gl_errors()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        view_matrix = self.camera.calculate_view_matrix()
        glLoadMatrixf(view_matrix)

        if self.cinematic and self.cinematic.playing_cinematic:
            self.cinematic.render_frame()
        else:
            self.scene_manager.render_scene(self.viewport_width, self.viewport_height, self.camera)

            # Dessiner les boutons et le rectangle
            glDisable(GL_DEPTH_TEST)  # Empêche la scène 3D de masquer les boutons
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, self.viewport_width, 0, self.viewport_height)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            # Dessiner le menu actuel
            self.menu_manager.draw_current_menu()

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glEnable(GL_DEPTH_TEST)  # Réactiver après que les boutons aient été dessinés

            # Dessiner le texte en bas à droite
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(self.viewport_width - 253, 10)
            for char in "Powered by Slashed Engine 1":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glutSwapBuffers()

    def reshape(self, width, height):
        aspect_ratio = self.screen_width / self.screen_height
        window_aspect_ratio = width / height

        if window_aspect_ratio > aspect_ratio:
            self.viewport_width = int(height * aspect_ratio)
            self.viewport_height = height
            self.viewport_x = (width - self.viewport_width) // 2
            self.viewport_y = 0
        else:
            self.viewport_width = width
            self.viewport_height = int(width / aspect_ratio)
            self.viewport_x = 0
            self.viewport_y = (height - self.viewport_height) // 2

        glViewport(self.viewport_x, self.viewport_y, self.viewport_width, self.viewport_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(self.viewport_width) / float(self.viewport_height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def mouse_click(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_left_pressed = True
                self.camera.last_mouse_x = x
                self.camera.last_mouse_y = y
                # Ajuster les coordonnées de la souris en fonction des bandes noires
                adjusted_x = (x - self.viewport_x) * (self.screen_width / self.viewport_width)
                adjusted_y = (y - self.viewport_y) * (self.screen_height / self.viewport_height)
                # Si une cinématique est en cours, on la skip
                if self.cinematic and self.cinematic.playing_cinematic:
                    self.cinematic.skip_cinematic = True
                else:
                    self.menu_manager.handle_click(adjusted_x, self.screen_height - adjusted_y)  # Inverser l'axe Y pour correspondre aux coordonnées de la fenêtre
            elif state == GLUT_UP:
                self.mouse_left_pressed = False

    def mouse_motion(self, x, y):
        if self.mouse_left_pressed and not self.menu_manager.is_menu_active():
            x_offset = x - self.camera.last_mouse_x
            y_offset = y - self.camera.last_mouse_y
            self.camera.rotate(x_offset, y_offset)
            self.camera.last_mouse_x = x
            self.camera.last_mouse_y = y
            glutPostRedisplay()

    def keyboard(self, key, x, y):
        if key == b'z':
            self.camera.move("forward", 0.1)
        elif key == b's':
            self.camera.move("backward", 0.1)
        elif key == b'q':
            self.camera.move("left", 0.1)
        elif key == b'd':
            self.camera.move("right", 0.1)
        glutPostRedisplay()

    def refresh_config(self, config):
        self.screen_width = config["resolution"]["width"]
        self.screen_height = config["resolution"]["height"]
        self.fullscreen = config["fullscreen"]
        glutReshapeWindow(self.screen_width, self.screen_height)
        if self.fullscreen:
            glutFullScreen()
        else:
            glutReshapeWindow(self.screen_width, self.screen_height)