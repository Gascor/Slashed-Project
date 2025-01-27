import logging
import pymysql
import requests
import paramiko
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QTabWidget, QComboBox, QHBoxLayout, QListWidget, QPlainTextEdit, QListWidgetItem, QLineEdit
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QTextCursor, QTextCharFormat
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from werkzeug.security import generate_password_hash
from utils.database import reset_database
from utils.resources import resource_path
from ui.monitoring_thread import MonitoringThread
from dotenv import load_dotenv
import os, re

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
load_dotenv()
# Define the SOFTWARE_VERSION variable
SOFTWARE_VERSION = "0.0.130a"
VPS1_HOST = os.getenv('VPS1_HOST')
VPS1_USER = os.getenv('VPS1_USER')
VPS1_PASSWORD = os.getenv('VPS1_PASSWORD')
VPS2_HOST = os.getenv('VPS2_HOST')
VPS2_USER = os.getenv('VPS2_USER')
VPS2_PASSWORD = os.getenv('VPS2_PASSWORD')
VENV_PATH = os.getenv('VENV_PATH')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

class AdminPanel(QMainWindow):
    def __init__(self, admin_username, admin_password, db_host, db_user, db_password, db_name):
        try:
            logging.debug("Initializing AdminPanel")
            super().__init__()
            self.admin_username = admin_username
            self.admin_password = admin_password
            self.db_host = db_host
            self.db_user = db_user
            self.db_password = db_password
            self.db_name = db_name
            self.current_server = None  # Variable to track the current server
            self.monitoring_thread = None  # Variable to track the monitoring thread
            self.ssh_clients = {}  # Dictionary to store SSH clients for each tab
            self.init_ui()
        except Exception as e:
            logging.error(f"Error initializing AdminPanel: {e}")


    def init_ui(self):
        logging.debug("Setting up UI")
        self.resize(800, 600)  # Set initial size but allow resizing
        self.setWindowTitle('Slashed Project - Management Console')
        
        # Set the window icon
        icon_path = resource_path("resources/app.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        # Create main layout
        main_layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_database_tab(), "Database Management")
        self.tabs.addTab(self.create_other_tab(), "Other Section 1")
        self.tabs.addTab(self.create_game_servers_tab(), "Game Servers")
        self.tabs.addTab(self.create_monitoring_tab(), "System Monitoring")
        self.tabs.addTab(self.create_remote_engine_tab(), "Remote Engine")

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

    def create_game_servers_tab(self):
        logging.debug("Creating game servers tab")
        tab = QWidget()
        layout = QHBoxLayout()

        # Left side: server list
        left_layout = QVBoxLayout()
        self.server_list = QListWidget(self)
        left_layout.addWidget(self.server_list)

        self.update_servers_button = QPushButton('Update Servers', self)
        self.update_servers_button.clicked.connect(self.update_servers)
        left_layout.addWidget(self.update_servers_button)

        self.update_servers()  # Initial update

        # Right side: server controls
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('Server Controls', self))

        self.restart_button = QPushButton('Restart Server', self)
        self.restart_button.clicked.connect(self.restart_server)
        right_layout.addWidget(self.restart_button)

        self.shutdown_button = QPushButton('Shutdown Server', self)
        self.shutdown_button.clicked.connect(self.shutdown_server)
        right_layout.addWidget(self.shutdown_button)

        self.status_label = QLabel('Status: Unknown', self)
        right_layout.addWidget(self.status_label)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        tab.setLayout(layout)
        return tab

    def update_servers(self):
        logging.debug("Updating game servers")
        try:
            response = requests.get('http://apigw-slashed-project.fr/servers')  # Replace with your API endpoint
            servers = response.json()
            self.server_list.clear()
            for server in servers:
                item = QListWidgetItem(f"{server['name']} - {server['status']}")
                if server['status'] == 'Online':
                    item.setBackground(QBrush(QColor('green')))
                elif server['status'] == 'Offline':
                    item.setBackground(QBrush(QColor('red')))
                else:
                    item.setBackground(QBrush(QColor('yellow')))
                self.server_list.addItem(item)
        except Exception as e:
            logging.error(f"Error updating game servers: {e}")
            QMessageBox.critical(self, "Error", f"Error updating game servers: {e}")

    def restart_server(self):
        logging.debug("Restarting server")
        # Implement server restart logic here
        self.status_label.setText('Status: Restarting')
        # Simulate status change
        QTimer.singleShot(2000, lambda: self.status_label.setText('Status: Online'))

    def shutdown_server(self):
        logging.debug("Shutting down server")
        # Implement server shutdown logic here
        self.status_label.setText('Status: Shutting down')
        # Simulate status change
        QTimer.singleShot(2000, lambda: self.status_label.setText('Status: Offline'))

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
        options = QFileDialog.Option.DontUseNativeDialog
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
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
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
                host=self.db_host,
                user=self.db_user,
                password=self.db_password
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

    def create_remote_engine_tab(self):
        logging.debug("Creating remote engine tab")
        tab = QWidget()
        layout = QVBoxLayout()

        self.server_list = QComboBox(self)
        self.server_list.addItem("SERVER_01_APIGW-SLASHED-PROJECT.FR")
        self.server_list.addItem("SERVER_02_SLASHED-PROJECT.FR")
        layout.addWidget(self.server_list)

        self.add_terminal_button = QPushButton('Add Terminal', self)
        self.add_terminal_button.clicked.connect(self.add_terminal_tab)
        layout.addWidget(self.add_terminal_button)

        self.remove_terminal_button = QPushButton('Remove Terminal', self)
        self.remove_terminal_button.clicked.connect(self.remove_terminal_tab)
        layout.addWidget(self.remove_terminal_button)

        self.terminal_tabs = QTabWidget(self)
        layout.addWidget(self.terminal_tabs)

        tab.setLayout(layout)
        return tab

    def add_terminal_tab(self):
        server = self.server_list.currentText()
        terminal_tab = QWidget()
        layout = QVBoxLayout()

        remote_terminal = QTextEdit(self)
        remote_terminal.setReadOnly(True)
        remote_terminal.setStyleSheet("""
            QTextEdit {
                background-color: black;
                color: white;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        layout.addWidget(remote_terminal)

        command_input = QLineEdit(self)
        command_input.setPlaceholderText("Enter command here...")
        command_input.returnPressed.connect(lambda: self.send_command_to_server(command_input, remote_terminal))
        layout.addWidget(command_input)

        terminal_tab.setLayout(layout)
        self.terminal_tabs.addTab(terminal_tab, server)
        self.connect_to_server(server, remote_terminal)

    def remove_terminal_tab(self):
        current_index = self.terminal_tabs.currentIndex()
        if current_index != -1:
            tab_text = self.terminal_tabs.tabText(current_index)
            if tab_text in self.ssh_clients:
                self.ssh_clients[tab_text].stop()
                del self.ssh_clients[tab_text]
            self.terminal_tabs.removeTab(current_index)

    def send_command_to_server(self, command_input, remote_terminal):
        command = command_input.text()
        if not command.strip():
            remote_terminal.append("Please enter a command to send.")
            return
        remote_terminal.append(f"Executing command: {command}")
        current_index = self.terminal_tabs.currentIndex()
        tab_text = self.terminal_tabs.tabText(current_index)
        if tab_text in self.ssh_clients:
            self.ssh_clients[tab_text].send_command(command)
        command_input.clear()

    def update_output(self, text, remote_terminal):
        self.append_text_with_color(remote_terminal, text)

    def connect_to_server(self, server, remote_terminal):
        logging.debug(f"Connecting to {server}")
        remote_terminal.append(f"Connecting to {server}...")
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if server == "SERVER_01_APIGW-SLASHED-PROJECT.FR":
                ssh_client.connect(VPS1_HOST, username=VPS1_USER, password=VPS1_PASSWORD)
            elif server == "SERVER_02_SLASHED-PROJECT.FR":
                ssh_client.connect(VPS2_HOST, username=VPS2_USER, password=VPS2_PASSWORD)
            remote_terminal.append(f"Connected to {server}.")
            self.start_ssh_session(server, ssh_client, remote_terminal)
        except Exception as e:
            logging.error(f"Error connecting to {server}: {e}")
            remote_terminal.append(f"Error connecting to {server}: {e}")

    def start_ssh_session(self, server, ssh_client, remote_terminal):
        ssh_channel = ssh_client.invoke_shell()
        ssh_thread = SSHThread(ssh_channel, remote_terminal)
        ssh_thread.output_received.connect(lambda output: self.update_terminal(output, remote_terminal))
        ssh_thread.start()
        self.ssh_clients[server] = ssh_thread

    def update_terminal(self, output, remote_terminal):
        self.append_text_with_color(remote_terminal, output)

    def append_text_with_color(self, text_edit, text):
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        clean_text = ansi_escape.sub('', text)

        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        text_edit.setTextCursor(cursor)

        format = QTextCharFormat()
        format.setForeground(QColor('white'))

        cursor.insertText(clean_text, format)

class CommandThread(QThread):
    signal_output = pyqtSignal(str)

    def __init__(self, ssh_client, command):
        super().__init__()
        self.ssh_client = ssh_client
        self.command = command

    def run(self):
        stdin, stdout, stderr = self.ssh_client.exec_command(self.command, get_pty=True)
        while True:
            line = stdout.readline()
            if not line:
                break
            self.signal_output.emit(line.strip())
        error = stderr.read().decode('utf-8')
        if error:
            self.signal_output.emit("Error:\n" + error)

class SSHThread(QThread):
    output_received = pyqtSignal(str)

    def __init__(self, ssh_channel, remote_terminal):
        super().__init__()
        self.ssh_channel = ssh_channel
        self.remote_terminal = remote_terminal
        self.active = True

    def run(self):
        while self.active:
            if self.ssh_channel.recv_ready():
                output = self.ssh_channel.recv(4096).decode('utf-8')
                self.output_received.emit(output)
            QThread.msleep(10)  # Reduce CPU load

    def send_command(self, command):
        self.ssh_channel.send(command + '\n')

    def stop(self):
        self.active = False
        self.ssh_channel.close()
