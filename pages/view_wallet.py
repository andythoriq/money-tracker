from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QGroupBox, QSpinBox, QMessageBox, QInputDialog
)
from controller.wallet import Wallet

class WalletView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Tombol kembali ke Dashboard
        self.btn_back = QPushButton("Kembali")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        # === BOX TAMBAH WALLET ===
        self.group_add_wallet = QGroupBox("Tambah Wallet")
        layout_add_wallet = QHBoxLayout()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nama Wallet")

        self.input_amount = QSpinBox()
        self.input_amount.setMaximum(1000000000)
        self.input_amount.setPrefix("Rp ")

        self.btn_add = QPushButton("Tambah")
        self.btn_add.clicked.connect(self.add_wallet)

        layout_add_wallet.addWidget(QLabel("Nama:"))
        layout_add_wallet.addWidget(self.input_name)
        layout_add_wallet.addWidget(QLabel("Saldo:"))
        layout_add_wallet.addWidget(self.input_amount)
        layout_add_wallet.addWidget(self.btn_add)

        self.group_add_wallet.setLayout(layout_add_wallet)
        layout.addWidget(self.group_add_wallet)

        # === TABEL WALLET ===
        self.table_wallet = QTableWidget()
        self.table_wallet.setColumnCount(4)  # Nama, Saldo, Aksi
        self.table_wallet.setHorizontalHeaderLabels(["Nama", "Saldo", "E", "D"])
        layout.addWidget(self.table_wallet)

        self.setLayout(layout)
        self.load_wallets()

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah Dashboard

    def load_wallets(self):
        """Memuat data wallet ke tabel"""
        wallets = self.wallet_controller.load_wallets()
        self.table_wallet.setRowCount(len(wallets))

        for row, wallet in enumerate(wallets):
            name_item = QTableWidgetItem(wallet[0])
            amount_item = QTableWidgetItem(f"Rp {wallet[1]}")

            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, n=wallet[0]: self.edit_wallet(n))

            btn_delete = QPushButton("Hapus")
            btn_delete.clicked.connect(lambda _, n=wallet[0]: self.delete_wallet(n))

            self.table_wallet.setItem(row, 0, name_item)
            self.table_wallet.setItem(row, 1, amount_item)
            self.table_wallet.setCellWidget(row, 2, btn_edit)
            self.table_wallet.setCellWidget(row, 3, btn_delete)

    def add_wallet(self):
        """Menambah wallet baru"""
        name = self.input_name.text().strip()
        amount = self.input_amount.value()

        if name:
            self.wallet_controller.add_wallet(name, amount)
            self.load_wallets()
            self.input_name.clear()
            self.input_amount.setValue(0)
        else:
            QMessageBox.warning(self, "Error", "Nama wallet tidak boleh kosong!")

    def edit_wallet(self, name):
        """Mengedit saldo wallet"""
        new_amount, ok = QInputDialog.getInt(self, "Edit Wallet", f"Saldo baru untuk {name}:", min=0)
        if ok:
            self.wallet_controller.edit_wallet(name, new_amount)
            self.load_wallets()

    def delete_wallet(self, name):
        """Menghapus wallet"""
        confirm = QMessageBox.question(
            self, "Konfirmasi", f"Apakah Anda yakin ingin menghapus wallet '{name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.wallet_controller.delete_wallet(name)
            self.load_wallets()
