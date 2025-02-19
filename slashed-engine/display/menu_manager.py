from display.menu import MainMenu, SettingsMenu
import winsound

class MenuManager:
    def __init__(self, game):
        self.game = game  # ✅ Ajout de self.game pour corriger l'erreur
        self.main_menu = MainMenu(self.switch_to_settings, game)
        self.settings_menu = SettingsMenu(self.switch_to_main_menu, game)
        self.current_menu = self.main_menu  # Menu affiché par défaut

    def switch_to_main_menu(self):
        self.current_menu = self.main_menu
        self.current_menu.adjust_menu_size()  # ✅ Met à jour la taille des boutons

    def switch_to_settings(self):
        self.current_menu = self.settings_menu
        self.current_menu.adjust_menu_size()  # ✅ Met à jour la taille des éléments

    def draw_current_menu(self):
        if self.current_menu:
            self.current_menu.draw()

    def handle_click(self, x, y):
        """ Délègue le clic au menu actuellement affiché """
        if self.current_menu:
            self.current_menu.handle_click(x, y)


    def play_background_music(self):
        winsound.PlaySound("slashed-engine/assets/sounds/menu_theme.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def stop_background_music(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
    
    def is_menu_active(self):
        return self.current_menu is not None  # Vérifie si un menu est affiché
