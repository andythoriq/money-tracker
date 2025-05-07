from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget
from controller.account import Account
from pages.Dashboard_v1_2 import Dashboard
import hashlib


class LoginScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_controller = Account()
        self.dashboard = Dashboard()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Money Tracker Login")
        self.setGeometry(100, 100, 360, 640)
        self.setStyleSheet("background-color: #1c1f26;")

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # Tombol Kembali
        btn_back = QtWidgets.QPushButton("←")
        btn_back.setStyleSheet("""
            background-color: transparent;
            color: #d3e9a3;
            font-size: 18px;
            border: none;
        """)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.stack.currentIndex() - 1)
        )
        layout.addWidget(btn_back, alignment=QtCore.Qt.AlignLeft)

        # Judul
        title = QtWidgets.QLabel("Money Tracker")
        title.setStyleSheet("color: #d3e9a3; font-size: 22px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Subjudul
        sub_title = QtWidgets.QLabel("Masuk untuk mulai mengatur keuangan kamu")
        sub_title.setStyleSheet("color: #d3e9a3; font-size: 13px;")
        sub_title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(sub_title)

        layout.addSpacing(30)

        # Input Email
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("Masukkan Email")
        self.email_input.setStyleSheet(self.input_style())
        layout.addWidget(self.email_input)

        layout.addSpacing(10)

        # Input Password
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Masukkan Password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        layout.addWidget(self.password_input)

        layout.addSpacing(20)

        # Tombol Login
        btn_login = QtWidgets.QPushButton("Login")
        btn_login.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
            color: #1c1f26;
            padding: 12px;
            border-radius: 20px;
            font-weight: bold;
        """)
        btn_login.clicked.connect(self.account_valid)
        layout.addWidget(btn_login)
        layout.addSpacing(10)

        # Lupa Password & Daftar
        footer_layout = QtWidgets.QHBoxLayout()

        lupa_password = QtWidgets.QLabel(
            "<a href='#' style='color:#b8e994;'>Lupa Password?</a>"
        )
        lupa_password.setStyleSheet("color: #d3e9a3;")
        lupa_password.setOpenExternalLinks(False)
        footer_layout.addWidget(lupa_password)
        lupa_password.setAlignment(QtCore.Qt.AlignLeft)
        lupa_password.mousePressEvent = lambda event: self.stack.setCurrentIndex(4)

        register_page = QtWidgets.QLabel(
            "<a href='#' style='color:#b8e994;'>Belum Punya Akun</a>"
        )
        register_page.setStyleSheet("color: #d3e9a3;")
        register_page.setOpenExternalLinks(False)
        footer_layout.addWidget(register_page)
        register_page.setAlignment(QtCore.Qt.AlignRight)
        register_page.mousePressEvent = lambda event: self.stack.setCurrentIndex(2)

        layout.addLayout(footer_layout)

        self.setLayout(layout)

    def input_style(self):
        return """
            background-color: #2c2f36;
            color: #d3e9a3;
            padding: 8px;
            border: 1px solid #3a3d45;
            border-radius: 10px;
            font-size: 14px;
        """

    def display_error(self, widget, message):
        """Menampilkan pesan error pada input field"""
        widget.clear()
        widget.setStyleSheet(self.input_style() + "border: 1px solid #ff0000;")
        widget.setPlaceholderText(message)
        widget.setFocus()

    def account_valid(self):
        self.email_input.setStyleSheet(self.input_style())
        self.password_input.setStyleSheet(self.input_style())

        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email:
            self.display_error(self.email_input, "Email tidak boleh kosong")
            return False
        if "@" not in email or "." not in email.split("@")[-1]:
            self.display_error(self.email_input, "Format email tidak valid")
            return False
        if not password:
            self.display_error(self.password_input, "Password tidak boleh kosong")
            return False

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        account_info = self.account_controller.load_account()
        user = next((acc for acc in account_info if acc["email"] == email), None)

        if user is None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Email Tidak Ditemukan")
            msg.setText("Email yang Anda masukkan tidak terdaftar")
            msg.setStyleSheet(""" ... """)  # Tetap gunakan style yang sama

            btn_ubah = msg.addButton("Ubah", QtWidgets.QMessageBox.RejectRole)
            btn_daftar = msg.addButton("Daftarkan Email", QtWidgets.QMessageBox.AcceptRole)

            msg.exec_()
            if msg.clickedButton() == btn_daftar:
                self.stack.setCurrentIndex(2)
            return False

        if user["password"] != hashed_password:
            self.display_error(self.password_input, "Password salah")
            return False

        print("Login Berhasil")
        self.window().close()         # Gunakan ini agar window login tertutup
        self.dashboard.show()         # Dashboard ditampilkan
        return True

