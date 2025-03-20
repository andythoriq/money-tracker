from PyQt5.QtWidgets import QSplashScreen, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()

        # Set background image for splash screen
        pixmap = QPixmap("img/splashscreen.png") 
        self.setPixmap(pixmap)
        self.setWindowFlag(Qt.FramelessWindowHint) 

        # Optional: Add a loading message
        self.message = QLabel("Loading...", self)
        self.message.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.message.setStyleSheet("color: white; font-size: 14px;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.message)

    def set_loading_message(self, text):
        """Update the loading message dynamically."""
        self.message.setText(text)

    def mousePressEvent(self, event):
        """Override mousePressEvent to prevent closing on click."""
        pass  

