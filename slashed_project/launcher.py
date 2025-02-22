from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QLineEdit, QPushButton, QGroupBox, QWidget, QApplication
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import requests
import threading
from core.config import load_config
from slashed_game import SlashedGame
from display.cinematic import Cinematic
from utils.utils import configure_gpu, init_glut, register_callbacks
from display.update_item_widget import UpdateItemWidget  # Mise à jour de l'import
import sys

class GameLauncher(QObject):
    game_closed = pyqtSignal()

    def launch_game(self):
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
        cinematic_thread = threading.Thread(target=cinematic.play, args=('slashed_project/assets/video/cinematic.mp4',))
        cinematic_thread.start()

        game.run()  # Probablement appelle glutMainLoop() dans votre GameEngine
        game.check_gl_errors()  # Vérifie les erreurs après l'exécution du jeu

        # Émettre le signal lorsque le jeu se termine
        print("Game closed signal emitted")  # Debug message
        self.game_closed.emit()

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.game_launcher = GameLauncher()
        self.game_launcher.game_closed.connect(self.reopen_launcher)

    def init_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Slashed Project Launcher')

        # Set window icon
        self.setWindowIcon(QIcon('slashed_project/icon.png'))

        # Set background image
        self.setStyleSheet("QMainWindow {background-image: url('slashed_project/assets/textures/bg.png'); background-repeat: no-repeat; background-position: center;}")

        main_layout = QHBoxLayout()

        # Update Section
        updates_list = QListWidget()
        updates_list.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.populate_updates_list(updates_list)
        main_layout.addWidget(updates_list)

        # Login Section
        self.login_group_box = QGroupBox()
        self.login_layout = QVBoxLayout()
        logo_label = self.create_logo_label('slashed_project/assets/textures/WT-TB_2024_Logo.png', 450, 450)
        self.form_group_box = QGroupBox()
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(5)
        self.form_layout.setContentsMargins(10, 10, 10, 10)

        self.add_form_field("Email Address", "email_input", QLineEdit())
        self.add_form_field("Password", "password_input", QLineEdit(), QLineEdit.EchoMode.Password)
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        self.form_layout.addWidget(login_button)
        self.form_group_box.setLayout(self.form_layout)

        self.login_layout.addWidget(logo_label)
        self.login_layout.addWidget(self.form_group_box)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.form_group_box)
        center_layout.addStretch()

        self.login_layout.addLayout(center_layout)
        self.login_group_box.setLayout(self.login_layout)
        main_layout.addWidget(self.login_group_box)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_logo_label(self, image_path, width, height):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(image_path).scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return logo_label

    def add_form_field(self, label_text, object_name, widget, echo_mode=None):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        widget.setObjectName(object_name)
        widget.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 150);")
        if echo_mode:
            widget.setEchoMode(echo_mode)
        self.form_layout.addWidget(label)
        self.form_layout.addWidget(widget)

    def populate_updates_list(self, updates_list):
        try:
            response = requests.get("http://apigw-slashed-project.fr/update-list")
            response.raise_for_status()
            updates = response.json()
            for update in updates:
                item_widget = UpdateItemWidget(update)
                item = QListWidgetItem(updates_list)
                item.setSizeHint(item_widget.sizeHint())
                updates_list.addItem(item)
                updates_list.setItemWidget(item, item_widget)
        except requests.RequestException as e:
            updates_list.addItem(f"Failed to fetch updates: {e}")

    def login(self):
        username = self.findChild(QLineEdit, "email_input").text()
        password = self.findChild(QLineEdit, "password_input").text()
        print("Login attempt with:", username, password)  # Placeholder for actual login logic
        # Simulate successful login
        self.show_logged_in_ui()

    def show_logged_in_ui(self):
        self.clear_form_layout()
        self.add_logged_in_buttons()

    def clear_form_layout(self):
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def add_logged_in_buttons(self):
        play_button = QPushButton('Play')
        play_button.clicked.connect(self.play_game)
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout)
        self.form_layout.addWidget(play_button)
        self.form_layout.addWidget(logout_button)

    def play_game(self):
        print("Launching the game...")  # Placeholder for actual game launch logic
        self.close()  # Fermer la fenêtre du Launcher
        self.game_launcher.launch_game()

    def logout(self):
        print("Logging out...")  # Placeholder for actual logout logic
        self.show_login_ui()

    def show_login_ui(self):
        self.clear_form_layout()
        self.add_form_field("Email Address", "email_input", QLineEdit())
        self.add_form_field("Password", "password_input", QLineEdit(), QLineEdit.EchoMode.Password)
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)
        self.form_layout.addWidget(login_button)

    def reopen_launcher(self):
        print("Reopening launcher...")  # Debug message
        self.show()
        self.show_logged_in_ui()

def main():
    app = QApplication([])
    ex = Launcher()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()