from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QSpinBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from controller.outcome import Outcome
from controller.category import Category
from controller.wallet import Wallet

class OutcomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.outcome_controller = Outcome(Wallet())
        self.category_controller = Category()
        self.wallet_controller = Wallet()
        self.init_ui()

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

        layout.addWidget(QLabel("Masukkan Jumlah Pengeluaran"))
        layout.addWidget(self.input_amount)
        layout.addWidget(QLabel("Pilih Kategori"))
        layout.addWidget(self.input_category)
        layout.addWidget(QLabel("Pilih Sumber Pengeluaran"))
        layout.addWidget(self.input_wallet)
        layout.addWidget(QLabel("Deskripsi"))
        layout.addWidget(self.input_desc)
        layout.addWidget(QLabel("Input Tanggal"))
        layout.addWidget(self.input_date)

        self.btn_save = QPushButton("Simpan")
        self.btn_save.clicked.connect(self.add_outcome)
        layout.addWidget(self.btn_save)

        # Tombol kembali ke Dashboard
        self.btn_back = QPushButton("Kembali")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def refresh_inputs(self):
        """Memuat ulang QComboBox"""
        self.input_amount.setValue(0)
        self.input_desc.clear()
        self.input_date.clear()
        self.input_category.clear()
        self.input_wallet.clear()
        
        category_names = self.category_controller.load_category_names("outcome")
        wallets = self.wallet_controller.load_wallets()

        self.input_category.addItems(category_names)
        for wallet in wallets:
            self.input_wallet.addItem(f"{wallet[0]} - Rp {wallet[1]}", wallet[0])

    def add_outcome(self):
        """Menambahkan pengeluaran"""
        amount = self.input_amount.value()
        category = self.input_category.currentText().strip()
        wallet = self.input_wallet.currentData()
        desc = self.input_desc.text().strip()
        date = self.input_date.text().strip()
        if amount:
            if self.outcome_controller.add_outcome(amount, category, wallet, desc, date) == False:
                print("Gagal menambahkan data (perhatikan jumlah uang yang dimasukkan!)")

            self.refresh_inputs()
        else:
            print("Jumlah tidak boleh kosong!")

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah Dashboard
