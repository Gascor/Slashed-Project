from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
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