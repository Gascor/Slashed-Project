import json
from display.gui import Button, Dropdown
from OpenGL.GLUT import *
import winsound
from core.config import load_config, save_config  # ✅ Ajout de save_config
from utils.shapes.rectangle import Rectangle  # ✅ Ajoute cet import en haut du fichier



# ✅ Charger les positions depuis le JSON
def load_ui_positions():
    with open("slashed-engine/display/ui_positions.json", "r") as file:
        return json.load(file)
    
class Menu:
    def __init__(self, game):
        self.buttons = []
        self.dropdowns = []
        self.game = game  # ✅ Ajout de game pour avoir les dimensions correctes

        # ✅ Adapter le rectangle à la taille de l'écran
        screen_width = self.game.viewport_width
        screen_height = self.game.viewport_height

        self.rectangle = Rectangle(0, 0, screen_width, screen_height)

    def adjust_menu_size(self):
        """ Ajuste dynamiquement la taille et la position des boutons selon la résolution et le ratio """
        
        width = self.game.viewport_width
        height = self.game.viewport_height
        aspect_ratio = self.game.config["aspect-ratio"]

        # ✅ Adapter la taille des boutons en fonction du ratio
        if aspect_ratio == "16:9":
            button_width = width * 0.3
            button_height = height * 0.08
            button_x = width * 0.5 - button_width / 2
            button_y_start = height * 0.75
            button_y_step = height * 0.12

        elif aspect_ratio == "16:10":
            button_width = width * 0.28
            button_height = height * 0.07
            button_x = width * 0.5 - button_width / 2
            button_y_start = height * 0.78
            button_y_step = height * 0.11

        else:  # ✅ 4:3 par défaut
            button_width = width * 0.25
            button_height = height * 0.07
            button_x = width * 0.5 - button_width / 2
            button_y_start = height * 0.8
            button_y_step = height * 0.1

        print(f"Adjusting menu size: {width}x{height}, Button start: {button_x}, {button_y_start}")

        for i, button in enumerate(self.buttons):
            new_x = button_x
            new_y = button_y_start - i * button_y_step
            button.adjust_size(new_x, new_y, button_width, button_height)
            print(f"Updated button '{button.label}' -> ({new_x}, {new_y}) size ({button_width}x{button_height})")

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
        print(f"Checking button clicks at adjusted coordinates: ({x}, {y})")
        for dropdown in self.dropdowns:
            if dropdown.handle_click(x, y):
                # Fermer les autres dropdowns
                for other_dropdown in self.dropdowns:
                    if other_dropdown != dropdown:
                        other_dropdown.close()
                return
        for button in self.buttons:
            print(f"Button '{button.label}' position: ({button.x}, {button.y}) with size ({button.width}x{button.height})")
            if button.is_inside(x, y):
                button.click()

class MainMenu(Menu):
    def __init__(self, switch_to_settings, game):
        super().__init__(game)  # ✅ On passe seulement `game`
        self.config = load_config()  # Charger la config actuelle
        self.ui_positions = load_ui_positions()  # Charger les positions UI
        self.game = game

        # ✅ Récupérer la résolution et le ratio actuel
        aspect_ratio = self.config["aspect-ratio"]
        resolution = f'{self.config["resolution"]["width"]}x{self.config["resolution"]["height"]}'

        # ✅ Vérifier si la résolution est définie dans le JSON
        if aspect_ratio in self.ui_positions and resolution in self.ui_positions[aspect_ratio]:
            positions = self.ui_positions[aspect_ratio][resolution]
        else:
            print(f"❌ Résolution {resolution} non définie dans le JSON ! Utilisation des valeurs par défaut.")
            positions = {}

        # ✅ Fonction pour récupérer les valeurs avec fallback
        def get_pos(label, default):
            return positions.get(label, default)

        # ✅ Ajouter les boutons avec les positions dynamiques
        self.add_button(Button(
            label="Singleplayer",
            x=get_pos("Singleplayer", {"x": 150})["x"],
            y=get_pos("Singleplayer", {"y": 950})["y"],
            width=get_pos("Singleplayer", {"width": 500})["width"],
            height=get_pos("Singleplayer", {"height": 70})["height"],
            callback=self.start_game
        ))
            
        self.add_button(Button("Multiplayer", callback=self.multiplayer, **get_pos("Multiplayer", {"x": 150, "y": 850, "width": 500, "height": 70})))
        self.add_button(Button("Settings", callback=switch_to_settings, **get_pos("Settings", {"x": 150, "y": 750, "width": 500, "height": 70})))
        self.add_button(Button("About", callback=self.about, **get_pos("About", {"x": 150, "y": 650, "width": 500, "height": 70})))
        self.add_button(Button("Quit", callback=self.exit_game, **get_pos("Quit", {"x": 150, "y": 550, "width": 500, "height": 70})))

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
        super().__init__(game)
        self.add_button(Button("Apply", 600, 150, 400, 70, self.apply_settings))
        self.add_button(Button("Back", 150, 150, 400, 70, switch_to_main_menu))
        
        self.config = load_config()
        self.game = game

        # Définition des options disponibles pour aspect ratio, résolution, et mode d'affichage
        self.aspect_ratios = ["4:3", "16:9", "16:10"]
        self.resolutions = {
            "4:3": ["1024x768", "1280x960", "1600x1200"],
            "16:9": ["1280x720", "1920x1080", "2560x1440"],
            "16:10": ["1280x800", "1920x1200", "2560x1600"]
        }
        self.display_modes = ["Fullscreen", "Windowed"]
        self.gpu_options = ["Default", "Intel", "NVIDIA", "AMD"]

        # Charger les valeurs actuelles
        current_aspect = self.config["aspect-ratio"]
        current_resolution = f'{self.config["resolution"]["width"]}x{self.config["resolution"]["height"]}'
        current_display_mode = "Fullscreen" if self.config["fullscreen"] else "Windowed"
        current_gpu = self.config.get("gpu", "Default")

        # Définir les Dropdowns avec valeurs par défaut
        self.aspect_ratio_dropdown = Dropdown("Aspect Ratio", 600, 500, 400, 70, self.aspect_ratios, self.set_aspect_ratio)
        self.aspect_ratio_dropdown.selected_index = self.aspect_ratios.index(current_aspect)

        self.resolution_dropdown = Dropdown("Resolution", 600, 400, 400, 70, self.resolutions[current_aspect], self.set_resolution)
        if current_resolution in self.resolutions[current_aspect]:
            self.resolution_dropdown.selected_index = self.resolutions[current_aspect].index(current_resolution)

        self.display_mode_dropdown = Dropdown("Display Mode", 600, 300, 400, 70, self.display_modes, self.set_display_mode)
        self.display_mode_dropdown.selected_index = self.display_modes.index(current_display_mode)
        
        self.gpu_dropdown = Dropdown("GPU", 600, 200, 400, 70, self.gpu_options, self.set_gpu)
        self.gpu_dropdown.selected_index = self.gpu_options.index(current_gpu)

        # Ajouter les Dropdowns au menu
        self.add_dropdown(self.aspect_ratio_dropdown)
        self.add_dropdown(self.resolution_dropdown)
        self.add_dropdown(self.display_mode_dropdown)
        self.add_dropdown(self.gpu_dropdown)

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

    def set_gpu(self, gpu_choice):
        self.config["gpu"] = gpu_choice

    def apply_settings(self):
        print("Apply settings button clicked")
        save_config(self.config)
        self.game.refresh_config(self.config)
        self.adjust_menu_size()
        
    def adjust_menu_size(self):
        width = self.game.viewport_width
        height = self.game.viewport_height

        button_width = width * 0.25  # Ajustement pour correspondre au ratio d'écran
        button_height = height * 0.07
        button_x = width * 0.5 - button_width / 2  # Centrer le bouton
        button_y_start = height * 0.8  # Ajustement en bas de l'écran
        button_y_step = height * 0.1

        print(f"Adjusting menu size: {width}x{height}, Button start: {button_x}, {button_y_start}")

        for i, button in enumerate(self.buttons):
            new_x = button_x
            new_y = button_y_start - i * button_y_step
            button.adjust_size(new_x, new_y, button_width, button_height)
            print(f"Updated button '{button.label}' -> ({new_x}, {new_y}) size ({button_width}x{button_height})")


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