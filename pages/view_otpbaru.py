from PyQt5 import QtCore, QtGui, QtWidgets
from controller.otp import Otp
from controller.account import Account
from pages.view_register import RegisterScreen


class Ui_accotp(QtWidgets.QWidget):
    def __init__(self, stack, key_dict, user_data):
        super().__init__()
        self.stack = stack
        self.user_data = user_data
        self.key_dict = key_dict
        self.account_controller = Account()
        self.register_controller = RegisterScreen(self.stack, user_data)
        self.setupUi(user_data)

    def setupUi(self, user_data):
        self.setGeometry(0, 0, 360, 640)
        self.setStyleSheet("background-color: #1c1f26; color: #d3e9a3;")

        self.otp_backend = Otp()

        # Layout utama
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header
        header_layout = QtWidgets.QHBoxLayout()

        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d3e9a3;
                font-size: 20px;
                border: none;
            }
        """)
        self.back_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.stack.currentIndex() - 1)
        )
        header_layout.addWidget(self.back_button)

        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Judul
        title_label = QtWidgets.QLabel("Kode telah dikirim!")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QtWidgets.QLabel(
            "Cek E-mail kamu dan masukan\nkode OTP untuk mendaftarkan akun"
        )
        subtitle_label.setStyleSheet("font-size: 16px;")
        subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        main_layout.addWidget(subtitle_label)

        # Input OTP
        otp_layout = QtWidgets.QVBoxLayout()

        otp_label = QtWidgets.QLabel("Kode OTP Anda")
        otp_label.setStyleSheet("font-size: 14px;")
        otp_layout.addWidget(otp_label)

        self.otp_input = QtWidgets.QLineEdit()
        self.otp_input.setStyleSheet("""
            QLineEdit {
                background-color: #2c2f36;
                color: #d3e9a3;
                border: 1px solid #3c3f46;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.otp_input.setPlaceholderText("Masukkan kode OTP")
        self.otp_input.textChanged.connect(self.verify_otp)
        otp_layout.addWidget(self.otp_input)

        main_layout.addLayout(otp_layout)

        # Pesan bantuan
        help_label = QtWidgets.QLabel(
            "Jika anda tidak menemukan email kode pendaftaran\n"
            "yang telah dikirimkan, cek juga folder spam email anda"
        )
        help_label.setStyleSheet("font-size: 12px; color: #8c8c8c;")
        help_label.setAlignment(QtCore.Qt.AlignCenter)
        help_label.setWordWrap(True)
        main_layout.addWidget(help_label)

        # Tombol kirim ulang
        resend_layout = QtWidgets.QHBoxLayout()

        resend_label = QtWidgets.QLabel("Kode OTP tidak diterima?")
        resend_label.setStyleSheet("font-size: 14px;")
        resend_layout.addWidget(resend_label)

        self.resend_button = QtWidgets.QPushButton("Kirim Ulang")
        self.resend_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7db16e;
                border: none;
                font-size: 14px;
            }
        """)
        self.resend_button.clicked.connect(self.send_otp)
        resend_layout.addWidget(self.resend_button)

        main_layout.addLayout(resend_layout)

        # Timer label
        self.timer_label = QtWidgets.QLabel()
        self.timer_label.setStyleSheet("font-size: 12px; color: #8c8c8c;")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.hide()
        main_layout.addWidget(self.timer_label)

        # Tombol lanjut
        self.continue_button = QtWidgets.QPushButton("Lanjutkan")
        self.continue_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
                color: #1c1f26;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        self.continue_button.clicked.connect(lambda: self.add_account(user_data))
        main_layout.addWidget(self.continue_button)

        main_layout.addStretch()
        self.setLayout(main_layout)

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_cooldown)

        # Kirim OTP pertama kali
        self.send_otp()

    def update_cooldown(self):
        cooldown_active, remaining_time = self.otp_backend.is_cooldown_active()
        if cooldown_active:
            self.timer_label.setText(
                f"Harap tunggu {remaining_time} detik sebelum mengirim OTP lagi"
            )
            self.timer_label.show()
            self.resend_button.setEnabled(False)
        else:
            self.timer_label.hide()
            self.resend_button.setEnabled(True)
            self.timer.stop()

    def send_otp(self):
        if self.otp_backend.startsmtp(self.user_data["email"], self.key_dict):
            self.timer.start(1000)
            self.back_button.setEnabled(False)

    def verify_otp(self):
        result = self.otp_backend.otpcheck(self.otp_input.text(), self.key_dict["key"])
        if result:
            self.continue_button.setEnabled(True)
            self.continue_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
                    color: #1c1f26;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }
            """)
        else:
            self.continue_button.setEnabled(False)
            self.continue_button.setStyleSheet("""
                QPushButton {
                    background-color: #2c2f36;
                    color: #d3e9a3;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    font-weight: bold;
                }
            """)

    def add_account(self, user_data):
        """Menambahkan akun baru setelah verifikasi OTP berhasil"""
        self.register_controller.add_account(user_data)
        self.stack.setCurrentIndex(0)
