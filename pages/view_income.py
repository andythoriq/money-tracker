from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QSpinBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QDate
from controller.income import Income
from controller.category import Category
from datetime import datetime
from controller.wallet import Wallet

class IncomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.income_controller = Income(Wallet())
        self.category_controller = Category()
        self.wallet_controller = Wallet()
        self.init_ui()

    def gettime(self):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        return QDate.fromString(date_str, "yyyy-MM-dd")

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_amount = QSpinBox()
        self.input_amount.setMinimum(0)
        self.input_amount.setMaximum(1000000000)
        self.input_amount.setPrefix("Rp ")
        self.input_amount.setSingleStep(50000)
        self.input_category = QComboBox()
        self.input_wallet = QComboBox()
        self.input_desc = QLineEdit()
        self.input_desc.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.input_date = QDateEdit()
        self.input_date.setDate(self.gettime())

        layout.addWidget(QLabel("Masukkan Jumlah Pemasukkan"))
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

    def refresh_inputs(self):
        self.input_amount.setValue(0)
        self.input_desc.clear()
        self.input_date.clear()

    def refresh_combobox(self):
        self.input_category.clear()
        self.input_wallet.clear()

        category_names = self.category_controller.load_category_names("income")
        wallets = self.wallet_controller.load_wallets()

        self.input_category.addItems(category_names)
        for wallet in wallets:
            self.input_wallet.addItem(f"{wallet[0]} - Rp {wallet[1]}", wallet[0])

    def add_income(self):
        """Menambahkan pemasukan"""
        amount = self.input_amount.value()
        category = self.input_category.currentText().strip()
        wallet = self.input_wallet.currentData()
        desc = self.input_desc.text().strip()
        date = self.input_date.text().strip()

        if amount:
            if self.income_controller.add_income(amount, category, wallet, desc, date) == False:
                print("Gagal menambahkan data")

            self.refresh_inputs()
            self.refresh_combobox()
        else:
            print("Jumlah tidak boleh kosong!")

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah Dashboard
