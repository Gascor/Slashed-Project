import os
import sys
from OpenGL.GLUT import *

def configure_gpu(config):
    """Configure the GPU based on the configuration."""
    gpu = config.get("gpu", "Default")
    if gpu == "NVIDIA":
        os.environ["NvOptimusEnablement"] = "1"
        print("Utilisation forcée du GPU NVIDIA.")
    elif gpu == "AMD":
        os.environ["AmdPowerXpressRequestHighPerformance"] = "1"
        print("Utilisation forcée du GPU AMD.")
    else:
        print("GPU par défaut utilisé.")

def init_glut(config):
    """Initialize GLUT with the given configuration."""
    glutInit(sys.argv)
    if config["fullscreen"]:
        mode_str = f'{config["resolution"]["width"]}x{config["resolution"]["height"]}:32@60'
        glutGameModeString(mode_str)
        if glutGameModeGet(GLUT_GAME_MODE_POSSIBLE):
            glutEnterGameMode()
        else:
            print("Game Mode not possible; fallback to windowed mode.")
            glutInitWindowSize(config["resolution"]["width"], config["resolution"]["height"])
    else:
        glutInitWindowSize(config["resolution"]["width"], config["resolution"]["height"])

def register_callbacks(game):
    """Register GLUT callbacks for the game."""
    glutDisplayFunc(game.display)
    glutIdleFunc(game.display)
    glutMouseFunc(game.mouse_click)
    glutMotionFunc(game.mouse_motion)
    glutKeyboardFunc(game.keyboard)
    glutReshapeFunc(game.reshape)