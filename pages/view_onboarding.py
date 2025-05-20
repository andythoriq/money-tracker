from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QStackedWidget, QWidget
import sys
from pages.view_login import LoginScreen
from pages.view_register import RegisterScreen
from pages.view_otpbaru import Ui_accotp
from pages.view_pemulihan import PemulihanScreen


class OnboardingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Money Tracker Onboarding")
        self.setGeometry(100, 100, 360, 640)
        self.setStyleSheet("background-color: #1c1f26;")

        # QStackedWidget
        self.stack = QStackedWidget(self)
        self.main_menu_widget = QtWidgets.QWidget()  # widget container untuk main menu
        self.init_main_menu()

        # Inisialisasi satu dictionary untuk semua data akun
        key_dict = {"key": ""} # Untuk OTP
        user_data = {
            "email": "",
            "username": "",
            "gender": "",
            "birth_date": "",
            "phone": "",
            "password": "",
        }

        # Tambahkan halaman ke stack
        self.otp_backend = Ui_accotp(self.stack, key_dict, user_data)
        self.login_view = LoginScreen(self.stack)
        self.register_view = RegisterScreen(self.stack, user_data)
        self.register_email = self.register_view.register_email_view(user_data)
        self.register_password = self.register_view.register_password_view()
        self.forgetPass_view = PemulihanScreen(self.stack, key_dict, user_data)
        self.forgetPass_password_view = self.forgetPass_view.new_password_UI()

        self.stack.addWidget(self.main_menu_widget)
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.register_view)
        self.stack.addWidget(self.register_email)
        self.stack.addWidget(self.register_password)
        self.stack.addWidget(self.otp_backend)
        self.stack.addWidget(self.forgetPass_view)
        self.stack.addWidget(self.forgetPass_password_view)

        # Layout utama window
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.stack)
        self.stack.setStyleSheet("background-color: #1c1f26;")
        self.setLayout(main_layout)

    def init_main_menu(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Gambar ilustrasi
        image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("illustration.png")
        pixmap = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(image_label)

        # Judul
        title = QtWidgets.QLabel("Jadikan hidupmu lebih teratur dengan Money Tracker!")
        title.setStyleSheet("color: #d3e9a3; font-size: 18px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Deskripsi
        desc = QtWidgets.QLabel(
            "Dari catatan pengeluaran sampai wishlist belanja, semua ada di sini."
        )
        desc.setStyleSheet("color: #d3e9a3; font-size: 13px;")
        desc.setWordWrap(True)
        desc.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(desc)

        layout.addSpacing(20)

        # Tombol Daftar
        btn_daftar = QtWidgets.QPushButton("Daftar")
        btn_daftar.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
            color: #1c1f26;
            padding: 10px;
            border-radius: 20px;
            font-weight: bold;
        """)
        btn_daftar.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.register_view)
        )
        layout.addWidget(btn_daftar)

        # Tombol Masuk
        btn_login = QtWidgets.QPushButton("Masuk")
        btn_login.setStyleSheet("""
            background-color: transparent;
            color: #d3e9a3;
            padding: 5px;
            font-size: 12px;
        """)
        btn_login.clicked.connect(lambda: self.stack.setCurrentWidget(self.login_view))
        layout.addWidget(btn_login)

        self.main_menu_widget.setLayout(layout)