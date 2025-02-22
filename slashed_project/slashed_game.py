from core.game_engine import GameEngine
from core.scene_manager import SceneManager
from display.menu_manager import MenuManager
from core.camera import Camera
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils.utils import register_callbacks
import threading
import time
from core.config import load_config

class SlashedGame(GameEngine):
    def __init__(self, screen_width, screen_height, fullscreen=True):
        super().__init__(screen_width, screen_height, fullscreen)
        self.config = load_config()  # Charge la configuration dès l'initialisation

        # Initialisation du viewport
        self.viewport_x_offset = 0
        self.viewport_y_offset = 0
        self.viewport_width = screen_width
        self.viewport_height = screen_height

        self.scene_manager = None
        self.menu_manager = MenuManager(self)
        self.camera = Camera(position=[0, 0, 5], target=[0, 0, 0], up=[0, 1, 0])
        self.mouse_left_pressed = False
        self.cinematic = None

        self.window_id = None  # <-- Déclaration indispensable

    def init_window(self):
        glutInitWindowSize(self.screen_width, self.screen_height)
        self.window_id = glutCreateWindow(b"Slashed Project")
        glutSetWindow(self.window_id)
        glutPositionWindow(100, 100)

    def init(self):
        # Si nous sommes en fullscreen et en Game Mode, la fenêtre a déjà été créée
        if not (self.fullscreen and glutGameModeGet(GLUT_GAME_MODE_ACTIVE)):
            self.init_window()  # Crée la fenêtre une seule fois
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
            glDisable(GL_DEPTH_TEST)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, self.viewport_width, 0, self.viewport_height)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            self.menu_manager.draw_current_menu()

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glEnable(GL_DEPTH_TEST)

            # Dessiner le texte en bas à droite
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(2.5, -2.05)
            for char in "Powered by Slashed Engine 1":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glutSwapBuffers()

    def reshape(self, width, height):
        """
        Ajuste le viewport. En mode fullscreen, on étire le rendu pour remplir l'écran,
        évitant ainsi les bandes noires. En mode windowed, on conserve le letterboxing
        pour respecter l'aspect ratio configuré.
        """
        if self.fullscreen and glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
            # Pour éviter les bandes noires, on utilise toute la taille de la fenêtre.
            # On peut utiliser soit les paramètres passés (width, height) soit ceux retournés par glutGameModeGet.
            # Ici, on utilise width et height qui devraient correspondre aux dimensions réelles du mode fullscreen.
            viewport_x = 0
            viewport_y = 0
            viewport_width = width
            viewport_height = height
        else:
            aspect_ratio = self.config["aspect-ratio"]
            aspect_ratios = {"4:3": 4/3, "16:9": 16/9, "16:10": 16/10}
            desired_ratio = aspect_ratios.get(aspect_ratio, width/height)
            window_ratio = width / height

            if window_ratio > desired_ratio:
                viewport_height = height
                viewport_width = int(height * desired_ratio)
                viewport_x = (width - viewport_width) // 2
                viewport_y = 0
            else:
                viewport_width = width
                viewport_height = int(width / desired_ratio)
                viewport_x = 0
                viewport_y = (height - viewport_height) // 2

        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        print(f"Viewport updated: {viewport_width}x{viewport_height}, Offset: ({viewport_x}, {viewport_y})")
        glViewport(viewport_x, viewport_y, viewport_width, viewport_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Pour le mode fullscreen, on utilise l'aspect calculé sur toute la fenêtre, ce qui évite les bandes noires.
        gluPerspective(45.0, float(viewport_width)/float(viewport_height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        if hasattr(self.menu_manager.current_menu, 'adjust_menu_size'):
            self.menu_manager.current_menu.adjust_menu_size()

    def update_viewport(self, width, height):
        if self.fullscreen and glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
            # Force l'utilisation de la résolution demandée
            width, height = self.screen_width, self.screen_height
        else:
            width, height = self.screen_width, self.screen_height
        self.reshape(width, height)

    def mouse_click(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_left_pressed = True
                self.camera.last_mouse_x = x
                self.camera.last_mouse_y = y

                norm_x = (x - self.viewport_x) / self.viewport_width
                norm_y = (y - self.viewport_y) / self.viewport_height
                adjusted_x = norm_x * self.viewport_width
                adjusted_y = (1 - norm_y) * self.viewport_height

                print(f"Mouse click at ({x}, {y}), adjusted to ({adjusted_x}, {adjusted_y})")
                if self.cinematic and self.cinematic.playing_cinematic:
                    self.cinematic.skip_cinematic = True
                else:
                    self.menu_manager.handle_click(adjusted_x, adjusted_y)
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
        previous_fullscreen = self.fullscreen
        previous_width, previous_height = self.screen_width, self.screen_height
        previous_ratio = self.config.get("aspect-ratio")

        self.config = config
        self.screen_width = config["resolution"]["width"]
        self.screen_height = config["resolution"]["height"]
        self.fullscreen = config["fullscreen"]
        new_ratio = config["aspect-ratio"]

        print(f"Applying new settings: {self.screen_width}x{self.screen_height}, "
            f"Fullscreen: {self.fullscreen}, Ratio: {new_ratio}")

        if (self.fullscreen != previous_fullscreen) or (self.screen_width != previous_width or self.screen_height != previous_height):

            # Si on passe de windowed (False) à fullscreen (True)
            if not previous_fullscreen and self.fullscreen:
                if self.window_id is not None:
                    print("Destroying existing windowed window before entering fullscreen")
                    glutDestroyWindow(self.window_id)
                    self.window_id = None

            # Si une fenêtre Game Mode est active, on la quitte
            if glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
                glutLeaveGameMode()
                # On tente de récupérer l'ID de la fenêtre restaurée
                restored_win = glutGetWindow()
                print(f"After leaving Game Mode, glutGetWindow() returned: {restored_win}")
                self.window_id = restored_win

            if self.fullscreen:
                # Passage en mode Game Mode (fullscreen)
                mode_str = f"{self.screen_width}x{self.screen_height}:32@60"
                print(f"🔄 Requesting Game Mode: {mode_str}")
                glutGameModeString(mode_str)
                if glutGameModeGet(GLUT_GAME_MODE_POSSIBLE):
                    glutEnterGameMode()
                    self.window_id = glutGetWindow()  # Nouvelle fenêtre en Game Mode
                    print(f"✅ Entered Game Mode, window ID: {self.window_id}")
                    # Enregistrement des callbacks pour la fenêtre Game Mode
                    register_callbacks(self)
                    # Mise à jour du viewport et réinitialisation d'OpenGL
                    gm_width = glutGameModeGet(GLUT_GAME_MODE_WIDTH)
                    gm_height = glutGameModeGet(GLUT_GAME_MODE_HEIGHT)
                    print(f"🔄 Forcing viewport update to: {gm_width}x{gm_height}")
                    self.update_viewport(gm_width, gm_height)
                    self.init_opengl()
                    if self.scene_manager:
                        self.scene_manager.init_scene()
                    glutPostRedisplay()
                else:
                    print("⚠️ Requested Game Mode not available, switching back to windowed mode")
                    self.fullscreen = False

            if not self.fullscreen:
                # En mode fenêtré, essayez de récupérer la fenêtre active
                current_win = glutGetWindow()
                if current_win != 0:
                    self.window_id = current_win
                    print(f"🔄 Using existing window (ID: {self.window_id}) in windowed mode")
                    glutSetWindow(self.window_id)
                    glutReshapeWindow(self.screen_width, self.screen_height)
                    glutPositionWindow(100, 100)
                else:
                    print("🔄 No active window found, creating new window in windowed mode")
                    glutInitWindowSize(self.screen_width, self.screen_height)
                    self.window_id = glutCreateWindow(b"Slashed Project")
                    glutSetWindow(self.window_id)
                    glutPositionWindow(100, 100)

                # Enregistrement des callbacks pour le mode fenêtré
                register_callbacks(self)
                glutReshapeWindow(self.screen_width, self.screen_height)
                glutPostRedisplay()

        # Mise à jour finale du viewport
        if self.fullscreen and glutGameModeGet(GLUT_GAME_MODE_ACTIVE):
            gm_width = int(glutGameModeGet(GLUT_GAME_MODE_WIDTH))
            gm_height = int(glutGameModeGet(GLUT_GAME_MODE_HEIGHT))
            self.update_viewport(gm_width, gm_height)
        else:
            self.update_viewport(self.screen_width, self.screen_height)

        self.init_opengl()
        if self.scene_manager:
            self.scene_manager.init_scene()

        if hasattr(self.menu_manager.current_menu, 'adjust_menu_size'):
            self.menu_manager.current_menu.adjust_menu_size()

        print("✅ Graphics settings applied successfully!")