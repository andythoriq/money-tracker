from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

class PopupWarning(QMessageBox):
    def __init__(self, title, message, icon_path=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)

        # Menambahkan ikon kustom jika diberikan
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        self.exec_()