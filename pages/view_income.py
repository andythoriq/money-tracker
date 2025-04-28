from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, 
    QComboBox, QSpinBox, QFormLayout, QCalendarWidget,
    QLabel, QHBoxLayout
)
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QDate, Qt, QCoreApplication
from controller.income import Income
from controller.category import Category
from controller.wallet import Wallet
from controller.Popup import PopupWarning, PopupSuccess

class IncomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.income_controller = Income(Wallet())
        self.category_controller = Category()
        self.wallet_controller = Wallet()
        self.init_ui()

    def init_income(self):
        self.setGeometry(340, 0, 1263, 900)

    def init_ui(self):
        self.setGeometry(340, 0, 1263, 900)
        
        # Main container
        main_container = QWidget()
        main_container.setObjectName("container")
        main_layout = QVBoxLayout()
        
        # Header
        self.header_label = QLabel("Income Baru")
        self.header_label.setObjectName("Label_1")
        
        # Form container
        form_container = QWidget()
        form_container.setObjectName("Layout")
        form_layout = QFormLayout()
        
        # Input jumlah pemasukan container
        amount_container = QWidget()
        amount_layout = QHBoxLayout()
        self.amount_label = QLabel("Jumlah Pemasukan:")
        self.amount_label.setObjectName("form_label")
        self.input_amount = QSpinBox()
        self.input_amount.setObjectName("form_input")
        self.input_amount.setMinimum(0)
        self.input_amount.setMaximum(1000000000)
        self.input_amount.setPrefix("Rp ")
        self.input_amount.setSingleStep(50000)
        amount_layout.addWidget(self.amount_label)
        amount_layout.addWidget(self.input_amount)
        amount_container.setLayout(amount_layout)

        category_wallet_container = QWidget()
        category_wallet_layout = QHBoxLayout()
        
        category_container = QWidget()
        category_layout = QVBoxLayout()
        self.category_label = QLabel("Kategori:")
        self.category_label.setObjectName("form_label")
        self.input_category = QComboBox()
        self.input_category.setObjectName("form_input")
        category_layout.addWidget(self.category_label)
        category_layout.addWidget(self.input_category)
        category_container.setLayout(category_layout)
        
        wallet_container = QWidget()
        wallet_layout = QVBoxLayout()
        self.wallet_label = QLabel("Dompet yang akan diisi:")
        self.wallet_label.setObjectName("form_label")
        self.input_wallet = QComboBox()
        self.input_wallet.setObjectName("form_input")
        wallet_layout.addWidget(self.wallet_label)
        wallet_layout.addWidget(self.input_wallet)
        wallet_container.setLayout(wallet_layout)
        
        category_wallet_layout.addWidget(category_container)
        category_wallet_layout.addWidget(wallet_container)
        category_wallet_container.setLayout(category_wallet_layout)

        # Description container
        desc_container = QWidget()
        desc_layout = QVBoxLayout()
        self.desc_label = QLabel("Deskripsi:")
        self.desc_label.setObjectName("form_label")
        self.input_desc = QLineEdit()
        self.input_desc.setObjectName("input_desc")
        self.input_desc.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.input_desc.setAlignment(Qt.AlignCenter)
        desc_layout.addWidget(self.desc_label)
        desc_layout.addWidget(self.input_desc)
        desc_container.setLayout(desc_layout)

        # Calendar container
        calendar_container = QWidget()
        calendar_layout = QVBoxLayout()
        self.calendar_label = QLabel("Masukkan Tanggal:")
        self.calendar_label.setObjectName("form_label")
        self.calendar = QCalendarWidget()
        self.calendar.setObjectName("calendar")
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        calendar_layout.addWidget(self.calendar_label)
        calendar_layout.addWidget(self.calendar)
        calendar_container.setLayout(calendar_layout)

        # Add to form layout
        form_layout.addRow(amount_container)
        form_layout.addRow(category_wallet_container)
        form_layout.addRow(desc_container)
        form_layout.addRow(calendar_container)
        
        # Buttons container
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("Simpan")
        self.btn_save.setObjectName("btn_save")
        self.btn_save.clicked.connect(self.add_income)
        
        self.btn_back = QPushButton("Kembali")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.clicked.connect(self.go_back)
        
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_back)
        buttons_container.setLayout(buttons_layout)
   
        form_container.setLayout(form_layout)
        
        main_layout.addWidget(self.header_label)
        main_layout.addWidget(form_container)
        main_layout.addWidget(buttons_container)
        
        main_container.setLayout(main_layout)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_container)
        self.setLayout(main_layout)

    def refresh_inputs(self):
        """Menghapus input setelah menyimpan"""
        self.input_amount.setValue(0)
        self.input_desc.clear()
        self.calendar.setSelectedDate(QDate.currentDate())  # Reset tanggal ke hari ini

    def refresh_combobox(self):
        """Memuat ulang kategori dan dompet"""
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
        date = self.calendar.selectedDate().toString("dd/MM/yyyy")  # Ambil tanggal dari kalender

    # Cek apakah ada yang kosong
        if amount == 0:
            PopupWarning("Warning", "Jumlah pemasukkan tidak boleh kosong")
            return
        if not category:
            PopupWarning("Warning", "Kategori tidak boleh kosong")
            return
        if not wallet:
            PopupWarning("Warning", "Dompet tidak boleh kosong")
            return
        if not desc:
            PopupWarning("Warning", "Deskripsi tidak boleh kosong")
            return
        
        if self.income_controller.add_income(amount, category, wallet, desc, date):
            self.refresh_inputs()
            self.refresh_combobox()
            PopupSuccess("Success", "Pemasukkan berhasil disimpan!")
        else:
            PopupWarning("Warning", "Gagal menyimpan pemasukkan!")

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah Dashboard

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.header_label.setText(_translate("Form", lang.get("income", {}).get("Title", "")))
            self.amount_label.setText(_translate("Form", lang.get("income", {}).get("form1", "")))
            self.category_label.setText(_translate("Form", lang.get("income", {}).get("form2", "")))
            self.wallet_label.setText(_translate("Form", lang.get("income", {}).get("form3", "")))
            self.desc_label.setText(_translate("Form", lang.get("income", {}).get("form4", "")))
            self.calendar_label.setText(_translate("Form", lang.get("income", {}).get("form5", "")))
            self.btn_save.setText(_translate("Form", lang.get("income", {}).get("btn1", "")))
            self.btn_back.setText(_translate("Form", lang.get("income", {}).get("btn2", "")))