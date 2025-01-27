import sys
import logging
import os
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QIcon
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