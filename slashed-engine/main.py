from slashed_game import SlashedGame
from display.cinematic import Cinematic
import OpenGL.GL as gl
from OpenGL.GLUT import *
import threading
from core.config import load_config

def main():
    config = load_config()
    game = SlashedGame(screen_width=config["resolution"]["width"], screen_height=config["resolution"]["height"], fullscreen=config["fullscreen"])
    game.init()  # Initialiser le contexte OpenGL avant de jouer la cinématique

    # Enregistrer la fonction de rappel d'affichage
    glutDisplayFunc(game.display)
    glutIdleFunc(game.display)
    glutMouseFunc(game.mouse_click)
    glutMotionFunc(game.mouse_motion)
    glutKeyboardFunc(game.keyboard)
    glutReshapeFunc(game.reshape)

    # Créer une instance de la classe Cinematic et l'affecter à game.cinematic
    cinematic = Cinematic(game)
    game.cinematic = cinematic  # ASSIGNATION IMPORTANTE
    cinematic_thread = threading.Thread(target=cinematic.play, args=('slashed-engine/assets/video/cinematic.mp4',))
    cinematic_thread.start()

    game.run()
    game.check_gl_errors()  # Vérifiez les erreurs après avoir exécuté le jeu

if __name__ == "__main__":
    main()