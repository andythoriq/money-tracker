from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class OnboardingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Money Tracker Onboarding")
        self.setGeometry(100, 100, 360, 640)
        self.setStyleSheet("background-color: #1c1f26;")  # dark background

        # Layout utama
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Gambar ilustrasi
        image_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("illustration.png")  # ilustrasi custom, sesuaikan path gambar kamu
        pixmap = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(image_label)

        # Judul
        title = QtWidgets.QLabel("Jadi si paling tau semuanya")
        title.setStyleSheet("color: #d3e9a3; font-size: 18px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Deskripsi
        desc = QtWidgets.QLabel("Dari catatan pengeluaran sampai wishlist belanja, semua ada di sini.")
        desc.setStyleSheet("color: #d3e9a3; font-size: 13px;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(desc)

        # Spacer
        layout.addSpacing(20)

        # Tombol Daftar/Masuk
        btn_login = QtWidgets.QPushButton("Daftar atau Masuk")
        btn_login.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
            color: #1c1f26;
            padding: 10px;
            border-radius: 20px;
            font-weight: bold;
        """)
        layout.addWidget(btn_login)

        # Tombol Lewati
        btn_skip = QtWidgets.QPushButton("Lewati")
        btn_skip.setStyleSheet("""
            background-color: transparent;
            color: #d3e9a3;
            padding: 5px;
            font-size: 12px;
        """)
        layout.addWidget(btn_skip)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = OnboardingScreen()
    window.show()
    sys.exit(app.exec_())
