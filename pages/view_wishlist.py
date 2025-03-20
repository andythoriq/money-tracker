import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QRadioButton, QLineEdit, QMessageBox, QSpinBox, QComboBox, QLabel, QDialog
)
from controller.wishlist import Wishlist
from controller.wallet import Wallet

class WishlistView(QWidget):
    def __init__(self, wallet_controller, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.wishlist_controller = Wishlist(Wallet())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # === Form Tambah Wishlist ===
        form_layout = QHBoxLayout()

        form_layout.addWidget(QLabel("Nama:"))
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)

        form_layout.addWidget(QLabel("Harga:"))
        self.price_input = QSpinBox()
        self.price_input.setRange(1, 10_000_000)  # Maksimum bisa disesuaikan
        self.price_input.setSingleStep(50_000)
        form_layout.addWidget(self.price_input)

        add_button = QPushButton("Tambah Wishlist")
        add_button.clicked.connect(self.add_wishlist)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # === Filter Berdasarkan Status ===
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Filter Status:"))

        self.all_status = QRadioButton("Semua")
        self.unfulfilled_status = QRadioButton("Belum Terpenuhi")
        self.fulfilled_status = QRadioButton("Sudah Terpenuhi")

        self.all_status.setChecked(True)

        status_layout.addWidget(self.all_status)
        status_layout.addWidget(self.unfulfilled_status)
        status_layout.addWidget(self.fulfilled_status)

        self.all_status.toggled.connect(self.load_wishlists)
        self.unfulfilled_status.toggled.connect(self.load_wishlists)
        self.fulfilled_status.toggled.connect(self.load_wishlists)

        layout.addLayout(status_layout)

        # === Filter Berdasarkan Wallet ===
        # wallet_layout = QHBoxLayout()
        # wallet_layout.addWidget(QLabel("Filter Wallet:"))

        # self.wallet_buttons = []
        # wallet_names = self.wallet_controller.load_wallet_names()

        # for wallet_name in wallet_names:
        #     btn = QRadioButton(wallet_name)
        #     btn.toggled.connect(self.load_wishlists)
        #     wallet_layout.addWidget(btn)
        #     self.wallet_buttons.append(btn)

        # layout.addLayout(wallet_layout)

        # === Tabel Wishlist ===
        self.wishlist_table = QTableWidget()
        self.wishlist_table.setColumnCount(6)  
        self.wishlist_table.setHorizontalHeaderLabels(["ID", "Nama", "Harga", "Status", "E", "D"])
        layout.addWidget(self.wishlist_table)

        self.load_wishlists()

        # === Tombol Kembali ===
        self.btn_back = QPushButton("Kembali ke Dashboard")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_wishlists(self):
        """Memuat data wishlist ke tabel berdasarkan filter"""
        wishlists = self.wishlist_controller.wishlists  

        # Filter status
        if self.unfulfilled_status.isChecked():
            wishlists = self.wishlist_controller.filter_wishlists(False)
        elif self.fulfilled_status.isChecked():
            wishlists = self.wishlist_controller.filter_wishlists(True)

        # # Filter wallet
        # selected_wallet = None
        # for btn in self.wallet_buttons:
        #     if btn.isChecked():
        #         selected_wallet = btn.text()
        #         break

        # if selected_wallet:
        #     wishlists = self.wishlist_controller.filter_by_wallet(selected_wallet)

        # Muat data ke tabel
        self.wishlist_table.setRowCount(len(wishlists))
        for row, wishlist in enumerate(wishlists):
            if len(wishlist) < 4:
                continue

            self.wishlist_table.setItem(row, 0, QTableWidgetItem(wishlist[0]))  # ID
            self.wishlist_table.setItem(row, 1, QTableWidgetItem(wishlist[1]))  # Nama
            self.wishlist_table.setItem(row, 2, QTableWidgetItem(wishlist[2]))  # Harga
            self.wishlist_table.setItem(row, 3, QTableWidgetItem(wishlist[3]))  # Status

            # Tombol Edit dan Hapus
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, id=wishlist[0]: self.show_edit_dialog(id))
            self.wishlist_table.setCellWidget(row, 4, edit_button)

            delete_button = QPushButton("Hapus")
            delete_button.clicked.connect(lambda _, id=wishlist[0], name=wishlist[1], price=wishlist[2]: self.delete_wishlist(id, name, price))
            self.wishlist_table.setCellWidget(row, 5, delete_button)

    def add_wishlist(self):
        """Menambahkan wishlist baru"""
        name = self.name_input.text().strip()
        price = self.price_input.value()

        if not name:
            QMessageBox.warning(self, "Error", "Nama tidak boleh kosong!")
            return

        self.wishlist_controller.add_wishlist(name, price, False)  # Status default False
        QMessageBox.information(self, "Sukses", "Wishlist berhasil ditambahkan!")

        self.load_wishlists()  # Muat ulang daftar wishlist
        self.name_input.clear()
        self.price_input.setValue(1)

    def show_edit_dialog(self, wishlist_id):
        """Menampilkan popup edit wishlist"""
        wishlist = next((w for w in self.wishlist_controller.wishlists if w[0] == wishlist_id), None)
        if not wishlist:
            QMessageBox.warning(self, "Error", "Wishlist tidak ditemukan!")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Wishlist")
        layout = QVBoxLayout()

        # Nama
        name_label = QLabel("Nama:")
        name_input = QLineEdit()
        name_input.setText(wishlist[1])
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        # Harga
        price_label = QLabel("Harga:")
        price_input = QSpinBox()
        price_input.setRange(1, 10_000_000)
        price_input.setSingleStep(50_000)
        price_input.setValue(int(wishlist[2]))
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Status
        status_label = QLabel("Status:")
        status_input = QComboBox()
        status_input.addItems(["false", "true"])
        status_input.setCurrentText(wishlist[3])
        layout.addWidget(status_label)
        layout.addWidget(status_input)

        # Tombol Simpan
        save_button = QPushButton("Simpan")
        save_button.clicked.connect(lambda: self.save_edit(dialog, wishlist_id, name_input.text(), price_input.value(), status_input.currentText()))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edit(self, dialog, wishlist_id, name, price, status):
        """Menyimpan hasil edit wishlist"""
        if not name:
            QMessageBox.warning(self, "Error", "Nama tidak boleh kosong!")
            return

        success = self.wishlist_controller.edit_wishlist(wishlist_id, name, price, status)
        if success:
            QMessageBox.information(self, "Sukses", "Wishlist berhasil diperbarui!")
            self.load_wishlists()
            dialog.accept()
        else:
            QMessageBox.warning(self, "Error", "Gagal mengupdate wishlist!")

    def delete_wishlist(self, wishlist_id, name, price):
        """Konfirmasi dan hapus wishlist"""
        confirm = QMessageBox.question(self, "Hapus Wishlist", f"Apakah Anda ingin menghapus {name} yang bernilai {price}?", 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success = self.wishlist_controller.delete_wishlist(wishlist_id)
            if success:
                QMessageBox.information(self, "Sukses", "Wishlist berhasil dihapus!")
                self.load_wishlists()
            else:
                QMessageBox.warning(self, "Error", "Gagal menghapus wishlist!")

    def go_back(self):
        self.parent().setCurrentIndex(0)
