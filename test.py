import sys
import paramiko
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class SSHClient(QWidget):
    def __init__(self, ip, username, password):
        super().__init__()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(ip, username=username, password=password)
        self.initUI()

    def initUI(self):
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)

        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(font)
        self.textEdit.setTextColor(QColor('green'))
        self.textEdit.setReadOnly(True)

        self.commandLine = QLineEdit(self)
        self.commandLine.setFont(font)
        self.commandLine.returnPressed.connect(self.onEnter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.commandLine)
        self.setLayout(layout)
        self.setWindowTitle('SSH Client')
        self.resize(600, 400)

    def onEnter(self):
        command = self.commandLine.text()
        self.commandLine.clear()
        self.thread = CommandThread(self.ssh, command)
        self.thread.signal_output.connect(self.update_output)
        self.thread.start()

    def update_output(self, text):
        self.textEdit.append(text)

    def closeEvent(self, event):
        self.ssh.close()
        super().closeEvent(event)

class CommandThread(QThread):
    signal_output = pyqtSignal(str)

    def __init__(self, ssh, command):
        super().__init__()
        self.ssh = ssh
        self.command = command

    def run(self):
        stdin, stdout, stderr = self.ssh.exec_command(self.command, get_pty=True)
        while True:
            line = stdout.readline()
            if not line:
                break
            self.signal_output.emit(line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ssh_client = SSHClient('54.37.11.118', 'ubuntu', 'Creeper78&')
    ssh_client.show()
    sys.exit(app.exec())
