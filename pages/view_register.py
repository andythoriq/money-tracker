import hashlib, re
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QCheckBox,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont, QColor, QPalette, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from controller.account import Account


class RegisterScreen(QtWidgets.QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.account_controller = Account()
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("background-color: #1c1f26;")
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tombol Kembali
        btn_back = QtWidgets.QPushButton("←")
        btn_back.setStyleSheet("""
            background-color: transparent;
            color: #d3e9a3;
            font-size: 18px;
            border: none;
        """)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back, alignment=QtCore.Qt.AlignLeft)

        # Judul
        title = QtWidgets.QLabel("Daftar Akun Money Tracker")
        title.setStyleSheet("color: #d3e9a3; font-size: 18px; font-weight: bold;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(15)

        # Input Nama
        self.input_name_label = QtWidgets.QLabel("Nama:")
        self.input_name_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        self.input_nama = QtWidgets.QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan Nama")
        self.input_nama.setStyleSheet(self.input_style())
        layout.addWidget(self.input_name_label)
        layout.addWidget(self.input_nama)

        # Gender
        gender_layout = QtWidgets.QHBoxLayout()
        gender_label = QtWidgets.QLabel("Gender:")
        gender_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        layout.addWidget(gender_label)

        self.radio_laki = QtWidgets.QRadioButton("Laki-laki")
        self.radio_laki.setStyleSheet("color: #d3e9a3;")
        gender_layout.addWidget(self.radio_laki)

        self.radio_perempuan = QtWidgets.QRadioButton("Perempuan")
        self.radio_perempuan.setStyleSheet("color: #d3e9a3;")
        gender_layout.addWidget(self.radio_perempuan)

        layout.addLayout(gender_layout)

        # Tanggal lahir
        self.date_edit_label = QtWidgets.QLabel("Tanggal Lahir:")
        self.date_edit_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setStyleSheet(self.input_style())
        layout.addWidget(self.date_edit_label)
        layout.addWidget(self.date_edit)

        # Nomor HP
        self.input_hp_label = QtWidgets.QLabel("Nomor Handphone:")
        self.input_hp_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        self.input_hp = QtWidgets.QLineEdit()
        self.input_hp.setPlaceholderText("Nomor Handphone")
        self.input_hp.setStyleSheet(self.input_style())
        self.input_hp.setValidator(QRegExpValidator(QRegExp("[0-9]+")))
        layout.addWidget(self.input_hp_label)
        layout.addWidget(self.input_hp)

        layout.addSpacing(10)

        # text changed
        self.input_nama.textChanged.connect(self.validate_input_register)
        self.input_hp.textChanged.connect(self.validate_input_register)
        self.date_edit.dateChanged.connect(self.validate_input_register)
        self.radio_laki.toggled.connect(self.validate_input_register)
        self.radio_perempuan.toggled.connect(self.validate_input_register)

        # Tombol Lanjut
        self.btn_lanjut = QtWidgets.QPushButton("Lanjut")
        self.btn_lanjut.setStyleSheet("""
            background-color: #2c2f36;
            color: #d3e9a3;
            padding: 12px;
            border-radius: 20px;
            font-weight: bold;
        """)
        self.btn_lanjut.setEnabled(False)
        self.btn_lanjut.clicked.connect(lambda: (self.validate_input_register, self.stack.setCurrentIndex(self.stack.currentIndex() + 1)))
        layout.addWidget(self.btn_lanjut)

        # Link sudah punya akun
        btn_login = QtWidgets.QPushButton("Sudah punya akun?")
        btn_login.setStyleSheet("""
            background-color: transparent;
            color: #d3e9a3;
            font-size: 13px;
        """)
        btn_login.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def register_email_view(self):
        """Menampilkan halaman pendaftaran"""
        widget = QtWidgets.QWidget()
        layoutHbox = QtWidgets.QHBoxLayout()
        layoutHbox.setAlignment(QtCore.Qt.AlignTop)

        self.setStyleSheet("background-color: #1c1f26;")
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

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

        layout.addSpacing(30)

        # Progress Indicator (3 steps)
        progress_layout = QHBoxLayout()
        self.step1 = QLabel("✔")
        self.step2 = QLabel("✔")
        self.step3 = QLabel("✔")

        for step in [self.step1, self.step2, self.step3]:
            step.setAlignment(Qt.AlignCenter)
            step.setFixedSize(30, 30)
            step.setStyleSheet(
                "border: 2px solid #c1c1c1; border-radius: 15px; color: #c1c1c1; background-color: transparent;"
            )
            # step.setContentsMargins(0,30,100,30)
        self.step1.setStyleSheet(
            "border: 2px solid #7db16e; border-radius: 15px; color: #7db16e; background-color: transparent;"
        )

        progress_layout.addWidget(self.step1)
        progress_layout.addWidget(self.step2)
        progress_layout.addWidget(self.step3)
        layout.addLayout(progress_layout)

        layout.addSpacing(20)

        # Title
        title = QLabel("Alamat Email")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #d3e9a3")
        layout.addWidget(title)

        layout.addSpacing(10)

        # Email input
        self.input_email_label = QtWidgets.QLabel("Email")
        self.input_email_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Masukkan Email")
        self.email_input.setStyleSheet(self.input_style())
        self.email_input_warning = QLabel("")
        self.email_input_warning.setStyleSheet(
            "color: #ff0000; font-size: 12px; padding-left: 5px;"
        )
        layout.addWidget(self.input_email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.email_input_warning)
        self.email_input_warning.hide()
        self.email_input.textChanged.connect(self.email_valid)
        layout.addSpacing(5)

        # Info
        info_label = QLabel(
            "Alamat email yang dimasukkan ini akan menjadi akun Money Tracker milikmu."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #c1c1c1; font-size: 12px;")
        layout.addWidget(info_label)

        layout.addSpacing(10)

        # Checkbox
        checkbox_layout = QHBoxLayout()
        self.email_checkbox = QCheckBox()
        self.email_checkbox.setChecked(True)
        self.email_checkbox.setStyleSheet(
            "QCheckBox::indicator { width: 25px; height: 25px;}"
        )
        email_text = QLabel(
            "Saya bersedia menerima email terkait akun Money Tracker dan layanannya"
        )
        email_text.setWordWrap(True)
        email_text.setStyleSheet("color: #c1c1c1; font-size: 12px;")
        email_text.setAlignment(QtCore.Qt.AlignLeft)

        checkbox_layout.addWidget(self.email_checkbox)
        checkbox_layout.addWidget(email_text)
        layout.addLayout(checkbox_layout)

        layout.addSpacing(20)

        # Continue button
        self.continue_button = QPushButton("Lanjutkan")
        self.continue_button.setStyleSheet("""
            background-color: #2c2f36;
            color: #d3e9a3;
            padding: 12px;
            border-radius: 20px;
            font-weight: bold;
        """)
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.stack.currentIndex() + 1)
        )
        layout.addWidget(self.continue_button)

        layout.addSpacing(30)

        # Agreement
        agreement = QLabel(
            'Dengan menekan tombol "Lanjutkan", kamu menyetujui bahwa data dan informasi Money Tracker ID milikmu akan digunakan sesuai Kebijakan Data Pribadi.'
        )
        agreement.setWordWrap(True)
        agreement.setStyleSheet("color: #7f8c8d; font-size: 11px;")

        layout.addWidget(agreement)

        widget.setLayout(layout)

        return widget

    def register_password_view(self):
        """Menampilkan halaman pembuatan password"""
        widget = QtWidgets.QWidget()
        layoutHbox = QtWidgets.QHBoxLayout()
        layoutHbox.setAlignment(QtCore.Qt.AlignTop)

        self.setStyleSheet("background-color: #1c1f26;")
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

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

        layout.addSpacing(30)

        # Progress Indicator (3 steps)
        progress_layout = QHBoxLayout()
        self.step1 = QLabel("✔")
        self.step2 = QLabel("✔")
        self.step3 = QLabel("✔")

        for step in [self.step1, self.step2, self.step3]:
            step.setAlignment(Qt.AlignCenter)
            step.setFixedSize(30, 30)
            step.setStyleSheet(
                "border: 2px solid #c1c1c1; border-radius: 15px; color: #c1c1c1; background-color: transparent;"
            )
            # step.setContentsMargins(0,30,100,30)
        self.step1.setStyleSheet(
            "border: 2px solid #7db16e; border-radius: 15px; color: #7db16e; background-color: transparent;"
        )
        self.step2.setStyleSheet(
            "border: 2px solid #7db16e; border-radius: 15px; color: #7db16e; background-color: transparent;"
        )

        progress_layout.addWidget(self.step1)
        progress_layout.addWidget(self.step2)
        progress_layout.addWidget(self.step3)
        layout.addLayout(progress_layout)

        layout.addSpacing(20)

        # Title
        title = QLabel("Buat password")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #d3e9a3")
        layout.addWidget(title)

        layout.addSpacing(10)

        # Password input
        self.input_password_label = QtWidgets.QLabel("Password")
        self.input_password_label.setStyleSheet("color: #d3e9a3; font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet(self.input_style())
        self.password_warning = QLabel("")
        self.password_warning.setStyleSheet("color: #ff0000; font-size: 12px;")
        self.password_warning.hide()
        layout.addWidget(self.input_password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_warning)

        layout.addSpacing(10)

        # Password confirmation input
        self.input_password_confirm_label = QtWidgets.QLabel("Konfirmasi password")
        self.input_password_confirm_label.setStyleSheet(
            "color: #d3e9a3; font-size: 14px;"
        )
        self.password_confirm_input = QLineEdit()
        self.password_confirm_input.setPlaceholderText("Ulangi password")
        self.password_confirm_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_confirm_input.setStyleSheet(self.input_style())
        self.password_confirm_warning = QLabel("")
        self.password_confirm_warning.setStyleSheet("color: #ff0000; font-size: 12px;")
        self.password_confirm_warning.hide()
        layout.addWidget(self.input_password_confirm_label)
        layout.addWidget(self.password_confirm_input)
        layout.addWidget(self.password_confirm_warning)

        layout.addSpacing(5)

        # text changed
        self.password_input.textChanged.connect(self.password_pair_validasi)
        self.password_confirm_input.textChanged.connect(self.password_pair_validasi)

        # Info Validasi Password
        info_label = QLabel(
            "Password harus terdiri dari kombinasi karakter huruf (a-z, A-Z) dan angka (0-9)."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #c1c1c1; font-size: 14px;")
        layout.addWidget(info_label)

        layout.addSpacing(10)

        # Continue button
        self.continue_button_password = QPushButton("Lanjutkan")
        self.continue_button_password.setStyleSheet("""
            background-color: #2c2f36;
            color: #d3e9a3;
            padding: 12px;
            border-radius: 20px;
            font-weight: bold;
        """)
        self.continue_button_password.setEnabled(False)
        self.continue_button_password.clicked.connect(lambda: self.stack.setCurrentIndex(self.stack.currentIndex() + 1))
        layout.addWidget(self.continue_button_password)

        layout.addSpacing(30)

        # Agreement
        agreement = QLabel(
            'Dengan menekan tombol "Lanjutkan", kamu menyetujui bahwa data dan informasi Money Tracker ID milikmu akan digunakan sesuai Kebijakan Data Pribadi.'
        )
        agreement.setWordWrap(True)
        agreement.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(agreement)

        widget.setLayout(layout)

        return widget

    def password_pair_validasi(self):
        """Validasi password"""
        password = self.password_input.text().strip()
        password_confirm = self.password_confirm_input.text().strip()
        is_password_valid = (bool(re.search(r'[A-Z]', password)) and 
                             bool(re.search(r'[A-Z]', password_confirm)) and 
                             bool(re.search(r'[0-9]', password)) and 
                             bool(re.search(r'[0-9]', password_confirm)) and 
                             password == password_confirm)

        if not len(password) >= 8:
            self.password_warning.setText("Password minimal 8 karakter")
            self.password_warning.show()
            self.password_confirm_warning.setText("Password minimal 8 karakter")
            self.password_confirm_warning.show()
            self.continue_button_password.setEnabled(False)
            self.continue_button_password.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)

        if not is_password_valid:
            self.password_warning.setText("Password harus terdiri dari huruf kapital dan angka")
            self.password_warning.show()
            self.password_confirm_warning.setText("Password harus terdiri dari huruf kapital dan angka")
            self.password_confirm_warning.show()
            self.continue_button_password.setEnabled(False)
            self.continue_button_password.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)

        if password != password_confirm:
            self.password_warning.setText("Password dan konfirmasi password harus sama")
            self.password_warning.show()
            self.password_confirm_warning.setText("Password dan konfirmasi password harus sama")
            self.password_confirm_warning.show()
            self.continue_button_password.setEnabled(False)
            self.continue_button_password.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)
        
        if (len(password) >= 8 and is_password_valid and password == password_confirm):
            self.password_warning.hide()
            self.password_confirm_warning.hide()
            self.continue_button_password.setEnabled(True)
            self.continue_button_password.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
                color: #1c1f26;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)

    def email_valid(self):
        """Validasi email"""
        email = self.email_input.text().strip()

        if "@" not in email or "." not in email.split("@")[-1]:
            self.email_input_warning.setText("Email tidak valid")
            self.email_input_warning.show()
            self.continue_button.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)
            
        if  self.account_controller.check_email_exists(email):
            self.email_input_warning.setText("Email sudah terdaftar")
            self.email_input_warning.show()
            self.continue_button.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)
        
        if not self.account_controller.check_email_exists(email) and ("@" in email and "." in email.split("@")[-1]):
            self.email_input_warning.setAlignment(QtCore.Qt.AlignLeft)
            self.email_input_warning.hide()
            self.continue_button.setEnabled(True)
            self.continue_button.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
                color: #1c1f26;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)


    def validate_input_register(self):
        """Validasi input"""
        
        input_gender = self.radio_laki.isChecked() or self.radio_perempuan.isChecked()

        if (self.input_nama.text() and self.date_edit.text() and self.input_hp.text() and input_gender):

            # Semua field terisi
            self.btn_lanjut.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7db16e, stop:1 #b8e994);
                color: #1c1f26;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)
            self.btn_lanjut.setEnabled(True)
        else:
            # Ada field yang kosong
            self.btn_lanjut.setEnabled(False)
            self.btn_lanjut.setStyleSheet("""
                background-color: #2c2f36;
                color: #d3e9a3;
                padding: 12px;
                border-radius: 20px;
                font-weight: bold;
            """)

    def add_account(self):
        """Menambahkan akun baru"""
        email = self.email_input.text().strip()
        username = self.input_nama.text().strip
        gender = "Laki-laki" if self.radio_laki.isChecked() else "Perempuan"
        birth_date = self.date_edit.text()
        phone_number = self.input_hp.text().strip()
        created_at = QtCore.QDate.currentDate().toString("yyyy-MM-dd")

        # Hash password using SHA-256
        password = hashlib.sha256(
            (self.password_input.text().strip()).encode()
        ).hexdigest()

        self.account_controller.add_account(
            email, username, password, gender, birth_date, phone_number, created_at
        )

    def input_style(self):
        return """
            background-color: #2c2f36;
            color: #d3e9a3;
            padding: 8px;
            border: 1px solid #3a3d45;
            border-radius: 10px;
            font-size: 14px;
        """