from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-language App")
        self.setGeometry(100, 100, 350, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Welcome!")  # Akan diupdate oleh controller
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.lang_select = QComboBox()
        self.layout.addWidget(self.lang_select)

        self.theme_select = QComboBox()
        self.theme_select.addItems(["light", "dark"])
        self.layout.addWidget(self.theme_select)

import sys
from PyQt5.QtWidgets import QApplication
# from view.main_view import MainView
from controller.setting import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = MainView()
    controller = MainController(view)

    view.show()
    sys.exit(app.exec_())