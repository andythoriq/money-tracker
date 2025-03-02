from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from controller.income import Income
from controller.category import Category
from controller.wallet import Wallet

class IncomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.income_controller = Income(Wallet())
        self.category_controller = Category()
        self.wallet_controller = Wallet()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_amount = QLineEdit()
        self.input_category = QComboBox()
        self.input_wallet = QComboBox()
        self.input_desc = QLineEdit()
        self.input_desc.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.input_date = QDateEdit()

        layout.addWidget(QLabel("Masukkan Jumlah"))
        layout.addWidget(self.input_amount)
        layout.addWidget(QLabel("Pilih Kategori"))
        layout.addWidget(self.input_category)
        layout.addWidget(QLabel("Pilih Tempat Penyimpanan"))
        layout.addWidget(self.input_wallet)
        layout.addWidget(QLabel("Deskripsi"))
        layout.addWidget(self.input_desc)
        layout.addWidget(QLabel("Input Tanggal"))
        layout.addWidget(self.input_date)

        self.btn_save = QPushButton("Simpan")
        self.btn_save.clicked.connect(self.add_income)
        layout.addWidget(self.btn_save)

        # Tombol kembali ke Dashboard
        self.btn_back = QPushButton("Kembali")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def refresh_combobox(self):
        """Memuat QComboBox"""
        self.input_category.clear()
        self.input_wallet.clear()
        category_names = self.category_controller.load_category_names("income")
        wallet_names = self.wallet_controller.load_wallet_names()
        self.input_category.addItems(category_names)
        self.input_wallet.addItems(wallet_names)

    def add_income(self):
        """Menambahkan pemasukan"""
        amount = self.input_amount.text().strip()
        category = self.input_category.currentText().strip()
        wallet = self.input_wallet.currentText().strip()
        desc = self.input_desc.text().strip()
        date = self.input_date.text().strip()
        if amount:
            self.income_controller.add_income(amount, category, wallet, desc, date)

            self.input_amount.clear()
            self.input_desc.clear()
            self.input_date.clear()
        else:
            print("Jumlah tidak boleh kosong!")

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah Dashboard
