import logging
import os
import pymysql
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt
from werkzeug.security import check_password_hash
from utils.resources import resource_path
from utils.database import verify_credentials

# Define the SOFTWARE_VERSION variable
SOFTWARE_VERSION = "0.0.123a"

class LoginDialog(QDialog):
    def __init__(self, db_host, db_user, db_password, db_name):
        super().__init__()
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(495, 330)
        self.setWindowTitle('Management Console - Login')

        layout = QVBoxLayout()
        
        # Set the window icon
        icon_path = resource_path("resources/app.ico")
        self.setWindowIcon(QIcon(icon_path))

        # Ajouter le logo en haut
        logo_label = QLabel(self)
        try:
            pixmap_path = resource_path("resources/imgs/WT-TB_2024_Logo.png")
            print(pixmap_path)
            if not os.path.exists(pixmap_path):
                raise FileNotFoundError(f"Image not found: {pixmap_path}")
            pixmap = QPixmap(pixmap_path)
            logo_label.setPixmap(pixmap)
            logo_label.setScaledContents(True)
        except Exception as e:
            logging.error(f"Error loading logo: {e}")
            logo_label.setText("Logo not found")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Title = QLabel("Management Console")
        Title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        layout.addWidget(Title)

        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.check_login)

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        form_layout.addWidget(login_button)

        layout.addLayout(form_layout)

        # Ajouter la version du logiciel en bas
        version_label = QLabel(f"Version: {SOFTWARE_VERSION}", self)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        self.setLayout(layout)

    def check_login(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        logging.debug(f"Login data received - Username: {self.username}")

        try:
            valid_credentials = verify_credentials(self.username, self.password, self.db_host, self.db_user, self.db_password, self.db_name)
            if valid_credentials:
                logging.debug("Login successful")
                self.accept()
            else:
                logging.debug("Login failed: Invalid credentials")
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except pymysql.MySQLError as err:
            logging.error(f"Database connection failed: {err}")
            QMessageBox.critical(self, "Database Error", f"Failed to connect to the database: {err}")
        except Exception as e:
            logging.error(f"Error during login process: {str(e)}")
            QMessageBox.critical(self, 'Login Error', 'An unexpected error occurred during login.')