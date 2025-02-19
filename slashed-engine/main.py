import os
import sys
from core.config import load_config
from slashed_game import SlashedGame
from display.cinematic import Cinematic
from utils.utils import configure_gpu, init_glut, register_callbacks
import threading

def main():
    # Charger la configuration
    config = load_config()
    
    # Configurer le GPU
    configure_gpu(config)

    # Initialiser GLUT
    init_glut(config)

    game = SlashedGame(
        screen_width=config["resolution"]["width"],
        screen_height=config["resolution"]["height"],
        fullscreen=config["fullscreen"]
    )
    game.init()  # Initialise le contexte OpenGL (sans recréer la fenêtre en Game Mode)

    # Enregistrer les callbacks sur la fenêtre active (celle de Game Mode ou celle créée par init_window)
    register_callbacks(game)

    cinematic = Cinematic(game)
    game.cinematic = cinematic  # ASSIGNATION IMPORTANTE
    cinematic_thread = threading.Thread(target=cinematic.play, args=('slashed-engine/assets/video/cinematic.mp4',))
    cinematic_thread.start()

    game.run()  # Probablement appelle glutMainLoop() dans votre GameEngine
    game.check_gl_errors()  # Vérifie les erreurs après l'exécution du jeu

if __name__ == "__main__":
    main()