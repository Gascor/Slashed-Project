import paramiko
import json
import time
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv
import os

load_dotenv()
# Define the SOFTWARE_VERSION variable
SOFTWARE_VERSION = "0.0.114a"
VPS1_HOST = os.getenv('VPS1_HOST')
VPS1_USER = os.getenv('VPS1_USER')
VPS1_PASSWORD = os.getenv('VPS1_PASSWORD')
VPS2_HOST = os.getenv('VPS2_HOST')
VPS2_USER = os.getenv('VPS2_USER')
VPS2_PASSWORD = os.getenv('VPS2_PASSWORD')
VENV_PATH = os.getenv('VENV_PATH')

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