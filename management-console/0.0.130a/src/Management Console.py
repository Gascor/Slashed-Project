import sys
import logging
import os
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from dotenv import load_dotenv
from ui.login_dialog import LoginDialog
from ui.admin_panel import AdminPanel
from utils.resources import resource_path

# Define the path to the .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

# Get database credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Capturer toutes les exceptions non traitées et les loguer.
    """
    logging.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))

# Définir le gestionnaire d'exceptions pour intercepter tout ce qui n'est pas attrapé
sys.excepthook = handle_exception

def main():
    app = QApplication(sys.argv)

    # Set the application icon
    icon_path = resource_path("resources/app.ico")
    app.setWindowIcon(QIcon(icon_path))

    # Apply dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #2E2E2E;
            color: white;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #3E3E3E;
            color: white;
        }
        QPushButton {
            background-color: #4E4E4E;
            color: white;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #5E5E5E;
        }
        QPushButton:pressed {
            background-color: #3E3E3E;
        }
        QComboBox {
            background-color: #3E3E3E;
            color: white;
            border-radius: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #4E4E4E;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #3E3E3E;
            color: white;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 5px;
        }
        QTabBar::tab:selected {
            background: #4E4E4E;
        }
    """)

    login_dialog = LoginDialog(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    login_dialog.setWindowIcon(QIcon(icon_path))  # Set the icon for the login dialog
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        logging.debug("Opening Admin Panel")
        try:
            admin_panel = AdminPanel(login_dialog.username, login_dialog.password, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
            admin_panel.setWindowIcon(QIcon(icon_path))  # Set the icon for the admin panel
            admin_panel.show()
            sys.exit(app.exec())
        except Exception as e:
            logging.error(f"Error opening Admin Panel: {e}")
    else:
        logging.debug("Login dialog rejected")

if __name__ == '__main__':
    main()