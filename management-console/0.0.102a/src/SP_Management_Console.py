import sys
import os
import logging
import pymysql
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QTabWidget, QDialog, QLineEdit, QFormLayout, QComboBox, QHBoxLayout
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QFont
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import paramiko
import json
import time
import traceback

script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the log file path to a writable directory
log_file_path = os.path.join(script_dir, 'app.log')

# Configurer la journalisation
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Set dark background for matplotlib plots
plt.style.use({
    'axes.facecolor': '#2E2E2E',
    'axes.edgecolor': 'white',
    'axes.labelcolor': 'white',
    'figure.facecolor': '#2E2E2E',
    'grid.color': 'gray',
    'text.color': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.titlecolor': 'white'
})

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
VPS1_HOST = os.getenv('VPS1_HOST')
VPS1_USER = os.getenv('VPS1_USER')
VPS1_PASSWORD = os.getenv('VPS1_PASSWORD')
VPS2_HOST = os.getenv('VPS2_HOST')
VPS2_USER = os.getenv('VPS2_USER')
VPS2_PASSWORD = os.getenv('VPS2_PASSWORD')
VENV_PATH = os.getenv('VENV_PATH')  # Chemin de l'environnement virtuel
SOFTWARE_VERSION = "0.0.102a"  # Version du logiciel

def resource_path(relative_path):
    """Get the absolute path to the resource."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(495, 330)
        self.setWindowTitle('Management Console - Login')

        layout = QVBoxLayout()

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
            valid_credentials = self.verify_credentials(self.username, self.password)
            if valid_credentials:
                logging.debug("Login successful")
                self.accept()
            else:
                logging.debug("Login failed: Invalid credentials")
                QMessageBox.warning(self, 'Error', 'Invalid credentials')
        except Exception as e:
            logging.error(f"Error during login process: {str(e)}")
            QMessageBox.critical(self, 'Login Error', 'An unexpected error occurred during login.')


    def verify_credentials(self, username, password):
        connection = None
        try:
            logging.debug(f"Trying to connect to the database at {DB_HOST} as {DB_USER}")
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            logging.debug(f"User fetched from database: {user}")
            if user and check_password_hash(user['password_hash'], password):
                return True
            return False
        except pymysql.MySQLError as err:
            logging.error(f"Database connection failed: {err}")
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
            return False
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            QMessageBox.critical(self, "Error", "An unexpected error occurred.")
            return False
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()


class MonitoringThread(QThread):
    data_fetched = pyqtSignal(dict)

    def __init__(self, host, user, password, venv_path):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.venv_path = venv_path
        self._is_running = True

    def run(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host, username=self.user, password=self.password, banner_timeout=300, timeout=300)

            while self._is_running:
                cpu_usage_str, cpu_error = self.ssh_command(ssh, "import psutil; print(psutil.cpu_percent())")
                ram_usage_str, ram_error = self.ssh_command(ssh, "import psutil; print(psutil.virtual_memory().percent)")
                net_io_str, net_io_error = self.ssh_command(ssh, "import psutil, json; print(json.dumps(psutil.net_io_counters()._asdict()))")

                if cpu_error or ram_error or net_io_error:
                    continue

                if cpu_usage_str and ram_usage_str and net_io_str:
                    cpu_usage = float(cpu_usage_str)
                    ram_usage = float(ram_usage_str)
                    net_io = json.loads(net_io_str)

                    data = {
                        'cpu_usage': cpu_usage,
                        'ram_usage': ram_usage,
                        'net_io': net_io
                    }
                    self.data_fetched.emit(data)
                time.sleep(1)

            ssh.close()
        except paramiko.SSHException as e:
            logging.error(f"SSH connection error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def ssh_command(self, ssh, command):
        stdin, stdout, stderr = ssh.exec_command(f"{self.venv_path}/bin/python3 -c \"{command}\"")
        result = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return result, error

    def stop(self):
        self._is_running = False
        self.wait()

class AdminPanel(QMainWindow):
    def __init__(self, admin_username, admin_password):
        try:
            logging.debug("Initializing AdminPanel")
            super().__init__()
            self.admin_username = admin_username
            self.admin_password = admin_password
            self.current_server = None  # Variable to track the current server
            self.monitoring_thread = None  # Variable to track the monitoring thread
            self.init_ui()
        except Exception as e:
            logging.error(f"Error initializing AdminPanel: {e}")

    def init_ui(self):
        logging.debug("Setting up UI")
        self.resize(800, 600)  # Set initial size but allow resizing
        self.setWindowTitle('Slashed Project - Management Console')

        # Create main layout
        main_layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_database_tab(), "Database Management")
        self.tabs.addTab(self.create_other_tab(), "Other Section 1")
        self.tabs.addTab(self.create_other_tab(), "Other Section 2")
        self.tabs.addTab(self.create_monitoring_tab(), "System Monitoring")

        # Add tab widget to main layout
        main_layout.addWidget(self.tabs)

        # Create footer layout
        footer_layout = QHBoxLayout()
        footer_text = QLabel(f"Version: {SOFTWARE_VERSION} | Slashed Project - All rights reserved", self)
        footer_text.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        footer_text.setStyleSheet("font-weight: bold;")
        footer_logo = QLabel(self)
        try:
            footer_pixmap = QPixmap(resource_path("resources/imgs/WT-TB_2024_Logo.png")).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            footer_logo.setPixmap(footer_pixmap)
        except Exception as e:
            logging.error(f"Error loading footer logo: {e}")
        footer_logo.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(footer_text)
        footer_layout.addWidget(footer_logo)

        # Add footer layout to main layout
        main_layout.addLayout(footer_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_database_tab(self):
        logging.debug("Creating database tab")
        tab = QWidget()
        layout = QVBoxLayout()

        self.sql_script_text = QTextEdit(self)
        self.sql_script_text.setPlaceholderText("SQL script will be displayed here...")
        execute_button = QPushButton('Execute SQL Script', self)
        execute_button.clicked.connect(self.execute_sql_script)
        import_button = QPushButton('Import SQL Script', self)
        import_button.clicked.connect(self.import_sql_script)
        reset_button = QPushButton('Reset Database', self)
        reset_button.clicked.connect(self.reset_database)

        layout.addWidget(QLabel('SQL Script:', self))
        layout.addWidget(self.sql_script_text)
        layout.addWidget(import_button)
        layout.addWidget(execute_button)
        layout.addWidget(reset_button)

        tab.setLayout(layout)
        return tab

    def create_other_tab(self):
        logging.debug("Creating other tab")
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Content for other section', self))
        tab.setLayout(layout)
        return tab

    def create_monitoring_tab(self):
        logging.debug("Creating monitoring tab")
        tab = QWidget()
        layout = QVBoxLayout()

        self.server_selector = QComboBox(self)
        self.server_selector.addItem("SERVER_01_APIGW-SLASHED-PROJECT.FR", (VPS1_HOST, VPS1_USER, VPS1_PASSWORD))
        self.server_selector.addItem("SERVER_02_SLASHED-PROJECT.FR", (VPS2_HOST, VPS2_USER, VPS2_PASSWORD))
        self.server_selector.currentIndexChanged.connect(self.update_monitoring)

        self.cpu_canvas = FigureCanvas(plt.Figure())
        self.ram_canvas = FigureCanvas(plt.Figure())
        self.network_canvas = FigureCanvas(plt.Figure())

        layout.addWidget(QLabel('Select Server:', self))
        layout.addWidget(self.server_selector)
        layout.addWidget(QLabel('CPU Usage:', self))
        layout.addWidget(self.cpu_canvas)
        layout.addWidget(QLabel('RAM Usage:', self))
        layout.addWidget(self.ram_canvas)
        layout.addWidget(QLabel('Network Usage:', self))
        layout.addWidget(self.network_canvas)

        self.cpu_ax = self.cpu_canvas.figure.add_subplot(111)
        self.ram_ax = self.ram_canvas.figure.add_subplot(111)
        self.network_ax = self.network_canvas.figure.add_subplot(111)

        self.cpu_data = []
        self.ram_data = []
        self.network_data = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitoring)
        self.timer.start(1000)  # Update every second

        tab.setLayout(layout)
        return tab

    def reset_charts(self):
        logging.debug("Resetting charts")
        self.cpu_data = []
        self.ram_data = []
        self.network_data = []

        self.cpu_ax.clear()
        self.ram_ax.clear()
        self.network_ax.clear()

        self.cpu_ax.set_title('CPU Usage (%)')
        self.ram_ax.set_title('RAM Usage (%)')
        self.network_ax.set_title('Network Usage')

        self.cpu_canvas.draw()
        self.ram_canvas.draw()
        self.network_canvas.draw()

    def update_monitoring(self):
        logging.debug("Updating monitoring")
        current_server = self.server_selector.currentData()
        if not current_server:
            return

        if current_server != self.current_server:
            self.reset_charts()  # Reset charts only when changing server
            self.current_server = current_server

            if self.monitoring_thread:
                self.monitoring_thread.stop()  # Stop the current monitoring thread

            host, user, password = current_server

            self.monitoring_thread = MonitoringThread(host, user, password, VENV_PATH)
            self.monitoring_thread.data_fetched.connect(self.update_charts)
            self.monitoring_thread.start()

    def update_charts(self, data):
        logging.debug("Updating charts with new data")
        cpu_usage = data['cpu_usage']
        ram_usage = data['ram_usage']
        net_io = data['net_io']

        # Update CPU usage
        self.cpu_data.append(cpu_usage)
        if len(self.cpu_data) > 60:
            self.cpu_data.pop(0)
        self.cpu_ax.clear()
        self.cpu_ax.plot(self.cpu_data, label='CPU Usage (%)')
        self.cpu_ax.legend()
        self.cpu_canvas.draw()

        # Update RAM usage
        self.ram_data.append(ram_usage)
        if len(self.ram_data) > 60:
            self.ram_data.pop(0)
        self.ram_ax.clear()
        self.ram_ax.plot(self.ram_data, label='RAM Usage (%)')
        self.ram_ax.legend()
        self.ram_canvas.draw()

        # Update Network usage
        self.network_data.append((net_io['bytes_sent'], net_io['bytes_recv']))
        if len(self.network_data) > 60:
            self.network_data.pop(0)
        sent_data = [data[0] for data in self.network_data]
        recv_data = [data[1] for data in self.network_data]
        self.network_ax.clear()
        self.network_ax.plot(sent_data, label='Bytes Sent')
        self.network_ax.plot(recv_data, label='Bytes Received')
        self.network_ax.legend()
        self.network_canvas.draw()

    def import_sql_script(self):
        logging.debug("Importing SQL script")
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import SQL Script", "", "SQL Files (*.sql);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                sql_script = file.read()
                self.sql_script_text.setText(sql_script)

    def execute_sql_script(self):
        logging.debug("Executing SQL script")
        sql_script = self.sql_script_text.toPlainText()
        if not sql_script:
            QMessageBox.warning(self, "Warning", "No SQL script to execute.")
            return

        connection = None
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=self.admin_username,
                password=self.admin_password,
                database=DB_NAME
            )
            cursor = connection.cursor()
            for result in cursor.execute(sql_script, multi=True):
                pass
            connection.commit()
            QMessageBox.information(self, "Success", "SQL script executed successfully.")
        except pymysql.MySQLError as err:
            logging.error(f"Error executing SQL script: {err}")
            QMessageBox.critical(self, "Error", f"Error: {err}")
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

    def reset_database(self):
        logging.debug("Resetting database")
        connection = None
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            # Générer le mot de passe haché pour GascorSU
            hashed_password = generate_password_hash('HanaInari78&')

            commands = [
                "DROP DATABASE IF EXISTS slashed_project",
                "CREATE DATABASE slashed_project",
                "USE slashed_project",
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                f"INSERT INTO users (username, password_hash) VALUES ('GascorSU', '{hashed_password}')",
                "CREATE USER IF NOT EXISTS 'GascorSU'@'%' IDENTIFIED BY 'HanaInari78&'",
                "GRANT ALL PRIVILEGES ON *.* TO 'GascorSU'@'%' WITH GRANT OPTION",
                "FLUSH PRIVILEGES"
            ]
            for command in commands:
                cursor.execute(command)
            connection.commit()
            QMessageBox.information(self, "Success", "Database reset successfully.")
        except pymysql.MySQLError as err:
            logging.error(f"Error resetting database: {err}")
            QMessageBox.critical(self, "Error", f"Error: {err}")
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            QMessageBox.critical(self, "Error", "An unexpected error occurred.")
        finally:
            if connection and connection.open:
                cursor.close()
                connection.close()

def handle_exception(exc_type, exc_value, exc_traceback):
    """
    Capturer toutes les exceptions non traitées et les loguer.
    """
    logging.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))

# Définir le gestionnaire d'exceptions pour intercepter tout ce qui n'est pas attrapé
sys.excepthook = handle_exception

def main():
    import sys
    from PyQt6.QtWidgets import QApplication, QDialog

    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        logging.debug("Opening Admin Panel")
        try:
            admin_panel = AdminPanel(login_dialog.username, login_dialog.password)
            admin_panel.show()
            sys.exit(app.exec())
        except Exception as e:
            logging.error(f"Error opening Admin Panel: {e}")
    else:
        logging.debug("Login dialog rejected")

if __name__ == '__main__':
    main()