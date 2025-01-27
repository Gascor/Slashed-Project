from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QLineEdit, QPushButton, QGroupBox
from PyQt6.QtGui import QPixmap, QImage, QFont
from PyQt6.QtCore import Qt
import requests
import base64

class UpdateItemWidget(QWidget):
    def __init__(self, update):
        super().__init__()
        layout = QVBoxLayout()

        # Decode the base64 image
        image_data = base64.b64decode(update['image'])
        image = QImage()
        image.loadFromData(image_data)
        pixmap = QPixmap.fromImage(image).scaled(585, 585, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Create image label
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create text label
        text_label = QLabel(f"Version {update['version']} : {update['title']}\n{update['description']}")
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: black;")  # Set the text color to black

        # Add labels to layout
        layout.addWidget(image_label)
        layout.addWidget(text_label)
        self.setLayout(layout)
        
class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle('Slashed Project Launcher')

        # Set background image
        self.setStyleSheet("QMainWindow {background-image: url('imgs/bg.png'); background-repeat: no-repeat; background-position: center;}")

        main_layout = QHBoxLayout()

        # Update Section
        updates_list = QListWidget()
        updates_list.setStyleSheet("background-color: rgba(255, 255, 255, 150);")
        self.populate_updates_list(updates_list)
        main_layout.addWidget(updates_list)

        # Login Section
        login_group_box = QGroupBox()
        login_layout = QVBoxLayout()
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('imgs/WT-TB_2024_Logo.png').scaled(450, 450, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_group_box = QGroupBox()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(5)
        form_layout.setContentsMargins(10, 10, 10, 10)

        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        email_input = QLineEdit()
        email_input.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 150);")
        password_label = QLabel("Password")
        password_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setStyleSheet("color: black; background-color: rgba(255, 255, 255, 150);")
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)

        form_layout.addWidget(email_label)
        form_layout.addWidget(email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(password_input)
        form_layout.addWidget(login_button)
        form_group_box.setLayout(form_layout)

        login_layout.addWidget(logo_label)
        login_layout.addWidget(form_group_box)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_group_box)
        center_layout.addStretch()

        login_layout.addLayout(center_layout)

        login_group_box.setLayout(login_layout)
        main_layout.addWidget(login_group_box)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


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

def main():
    app = QApplication([])
    ex = Launcher()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()
