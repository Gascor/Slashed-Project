from display.gui import Button, Dropdown
from utils.shapes.rectangle import Rectangle
from OpenGL.GLUT import *
import winsound
from core.config import load_config, save_config

class Menu:
    def __init__(self, x, y, width, height):
        self.buttons = []
        self.dropdowns = []
        self.rectangle = Rectangle(x, y, width, height)

    def add_button(self, button):
        self.buttons.append(button)

    def add_dropdown(self, dropdown):
        self.dropdowns.append(dropdown)

    def draw(self):
        self.rectangle.draw()
        for button in self.buttons:
            button.draw()
        # Dessiner les dropdowns en dernier pour qu'ils soient en avant-plan
        for dropdown in self.dropdowns:
            dropdown.draw()

    def handle_click(self, x, y):
        for dropdown in self.dropdowns:
            if dropdown.handle_click(x, y):
                # Fermer les autres dropdowns
                for other_dropdown in self.dropdowns:
                    if other_dropdown != dropdown:
                        other_dropdown.close()
                return
        for button in self.buttons:
            if button.is_inside(x, y):
                button.click()

class MainMenu(Menu):
    def __init__(self, switch_to_settings):
        super().__init__(100, 100, 600, 1240)
        self.add_button(Button("Singleplayer", 150, 950, 500, 70, self.start_game))
        self.add_button(Button("Multiplayer", 150, 850, 500, 70, self.multiplayer))
        self.add_button(Button("Settings", 150, 750, 500, 70, switch_to_settings))
        self.add_button(Button("About", 150, 650, 500, 70, self.about))
        self.add_button(Button("Quit", 150, 550, 500, 70, self.exit_game))

    def start_game(self):
        print("Start Game button clicked")
        winsound.PlaySound(None, winsound.SND_PURGE)  # Arrêter la musique de fond

    def multiplayer(self):
        print("Multiplayer button clicked")

    def about(self):
        print("About button clicked")

    def exit_game(self):
        print("Exit button clicked")
        winsound.PlaySound(None, winsound.SND_PURGE)  # Arrêter la musique de fond
        glutLeaveMainLoop()

class SettingsMenu(Menu):
    def __init__(self, switch_to_main_menu, game):
        super().__init__(100, 100, 2360, 1240)
        self.add_button(Button("Apply", 600, 150, 400, 70, self.apply_settings))
        self.add_button(Button("Back", 150, 150, 400, 70, switch_to_main_menu))
        self.config = load_config()
        self.game = game

        # Ajouter les listes déroulantes pour les résolutions, le mode d'affichage et le ratio d'aspect
        self.aspect_ratios = ["4:3", "16:9", "16:10"]
        self.resolutions = {
            "4:3": ["1024x768", "1280x960", "1600x1200"],
            "16:9": ["1280x720", "1920x1080", "2560x1440"],
            "16:10": ["1280x800", "1920x1200", "2560x1600"]
        }
        self.display_modes = ["Fullscreen", "Windowed"]

        self.add_dropdown(Dropdown("Aspect Ratio", 600, 500, 400, 70, self.aspect_ratios, self.set_aspect_ratio))
        self.resolution_dropdown = Dropdown("Resolution", 600, 400, 400, 70, self.resolutions[self.config["aspect-ratio"]], self.set_resolution)
        self.add_dropdown(self.resolution_dropdown)
        self.add_dropdown(Dropdown("Display Mode", 600, 300, 400, 70, self.display_modes, self.set_display_mode))

    def set_aspect_ratio(self, aspect_ratio):
        self.config["aspect-ratio"] = aspect_ratio
        self.resolution_dropdown.options = self.resolutions[aspect_ratio]
        self.resolution_dropdown.selected_index = 0

    def set_resolution(self, resolution):
        width, height = map(int, resolution.split('x'))
        self.config["resolution"]["width"] = width
        self.config["resolution"]["height"] = height

    def set_display_mode(self, mode):
        self.config["fullscreen"] = (mode == "Fullscreen")

    def apply_settings(self):
        print("Apply settings button clicked")
        save_config(self.config)
        self.game.refresh_config(self.config)
        self.adjust_menu_size()

    def adjust_menu_size(self):
        # Ajuster la taille des boutons et des autres éléments en fonction de la résolution sélectionnée
        width = self.config["resolution"]["width"]
        height = self.config["resolution"]["height"]
        button_width = width * 0.2
        button_height = height * 0.05
        button_x = width * 0.3
        button_y_start = height * 0.7
        button_y_step = height * 0.1

        for i, button in enumerate(self.buttons):
            button.adjust_size(button_x, button_y_start - i * button_y_step, button_width, button_height)

        dropdown_width = width * 0.2
        dropdown_height = height * 0.05
        dropdown_x = width * 0.3
        dropdown_y_start = height * 0.5
        dropdown_y_step = height * 0.1

        for i, dropdown in enumerate(self.dropdowns):
            dropdown.adjust_size(dropdown_x, dropdown_y_start - i * dropdown_y_step, dropdown_width, dropdown_height)

    def draw(self):
        self.rectangle.draw()
        for button in self.buttons:
            button.draw()
        # Dessiner les dropdowns en dernier pour qu'ils soient en avant-plan
        for dropdown in self.dropdowns:
            dropdown.draw()
        # Dessiner les options des dropdowns en dernier pour qu'elles soient en avant-plan
        for dropdown in self.dropdowns:
            if dropdown.expanded:
                dropdown.draw_options()