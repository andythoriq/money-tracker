import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QRadioButton, QLineEdit, QMessageBox, QSpinBox, QComboBox, QLabel, QDialog
)
from PyQt5.QtCore import Qt
from controller.wishlist import Wishlist
from controller.wallet import Wallet

class WishlistView(QWidget):
    def __init__(self, wallet_controller, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.wishlist_controller = Wishlist(Wallet())
        self.initUI()

    def initUI(self):
        # Main container with dark background
        main_container = QWidget()
        main_container.setObjectName("wishlist_container")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        # Title container
        title_container = QHBoxLayout()
        title_label = QLabel("Wishlist")
        title_label.setObjectName("Label_1")
        title_container.addWidget(title_label)
        title_container.addStretch()
        main_layout.addLayout(title_container)

        # Content container with green background
        content_container = QWidget()
        content_container.setObjectName("wishlist_content")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Form layout
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        # Name input
        name_label = QLabel("Nama:")
        name_label.setObjectName("wishlist_label")
        form_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setObjectName("wishlist_input")
        self.name_input.setFixedWidth(400)
        form_layout.addWidget(self.name_input)

        # Price input
        price_label = QLabel("Harga:")
        price_label.setObjectName("wishlist_label")
        form_layout.addWidget(price_label)
        
        self.price_input = QSpinBox()
        self.price_input.setObjectName("wishlist_input")
        self.price_input.setRange(0, 100_000_000)
        self.price_input.setSingleStep(50_000)
        self.price_input.setFixedWidth(400)
        form_layout.addWidget(self.price_input)

        # Add button
        add_button = QPushButton("Tambah Wishlist")
        add_button.setObjectName("wishlist_button")
        add_button.setFixedWidth(175)
        add_button.clicked.connect(self.add_wishlist)
        form_layout.addWidget(add_button)

        form_layout.addStretch()
        content_layout.addLayout(form_layout)

        # Filter status layout
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        
        filter_label = QLabel("Filter Status:")
        filter_label.setObjectName("wishlist_label")
        status_layout.addWidget(filter_label)

        # Radio buttons
        self.all_status = QRadioButton("Semua")
        self.unfulfilled_status = QRadioButton("Belum Terpenuhi")
        self.fulfilled_status = QRadioButton("Sudah Terpenuhi")

        for radio in [self.all_status, self.unfulfilled_status, self.fulfilled_status]:
            radio.setObjectName("wishlist_radio")
            status_layout.addWidget(radio)

        self.all_status.setChecked(True)

        status_layout.addStretch()

        self.all_status.toggled.connect(self.load_wishlists)
        self.unfulfilled_status.toggled.connect(self.load_wishlists)
        self.fulfilled_status.toggled.connect(self.load_wishlists)

        content_layout.addLayout(status_layout)

        # Table
        self.wishlist_table = QTableWidget()
        self.wishlist_table.setObjectName("wishlist_table")
        self.wishlist_table.setColumnCount(6)
        self.wishlist_table.setHorizontalHeaderLabels(["No.", "Nama", "Harga", "Status", "E", "D"])
        
        # Adjust column widths proportionally
        total_width = self.wishlist_table.viewport().width()
        self.wishlist_table.setColumnWidth(0, int(total_width * 0.05))  # 5% for No.
        self.wishlist_table.setColumnWidth(1, int(total_width * 0.69))  # 35% for Nama
        self.wishlist_table.setColumnWidth(2, int(total_width * 0.35))  # 20% for Harga
        self.wishlist_table.setColumnWidth(3, int(total_width * 0.34))  # 20% for Status
        self.wishlist_table.setColumnWidth(4, int(total_width * 0.15))  # 10% for Edit
        self.wishlist_table.setColumnWidth(5, int(total_width * 0.153))  # 10% for Delete

        self.wishlist_table.verticalHeader().setVisible(False)
        self.wishlist_table.setMinimumHeight(300)  # Set minimum height for table
        content_layout.addWidget(self.wishlist_table)

        self.load_wishlists()

        # Add content container to main layout
        main_layout.addWidget(content_container)

        # Back button container at bottom right
        back_button_container = QHBoxLayout()
        back_button_container.setContentsMargins(0, 10, 20, 20)
        back_button_container.addStretch()
        
        self.btn_back = QPushButton("Kembali ke Dashboard")
        self.btn_back.setObjectName("wishlist_button")
        self.btn_back.setFixedWidth(200)
        self.btn_back.clicked.connect(self.go_back)
        back_button_container.addWidget(self.btn_back)
        
        main_layout.addLayout(back_button_container)

        # Set the main container as the central widget
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(main_container)
        self.setLayout(outer_layout)

    def load_wishlists(self):
        """Memuat data wishlist ke tabel berdasarkan filter"""
        wishlists = self.wishlist_controller.wishlists  

        # Filter status
        if self.unfulfilled_status.isChecked():
            wishlists = self.wishlist_controller.filter_wishlists(False)
        elif self.fulfilled_status.isChecked():
            wishlists = self.wishlist_controller.filter_wishlists(True)

        # Muat data ke tabel
        self.wishlist_table.setRowCount(len(wishlists))
        for row, wishlist in enumerate(wishlists):
            if len(wishlist) < 4:
                continue

            self.wishlist_table.setItem(row, 0, QTableWidgetItem(wishlist[0]))  # ID
            self.wishlist_table.setItem(row, 1, QTableWidgetItem(wishlist[1]))  # Nama
            self.wishlist_table.setItem(row, 2, QTableWidgetItem(wishlist[2]))  # Harga
            
            # Konversi status dari boolean ke text
            status_text = "Sudah Terpenuhi" if wishlist[3] == "true" else "Belum Terpenuhi"
            self.wishlist_table.setItem(row, 3, QTableWidgetItem(status_text))  # Status

            # Tombol Edit dan Hapus
            edit_button = QPushButton("Edit")
            edit_button.setObjectName("wishlist_button")
            edit_button.clicked.connect(lambda _, id=wishlist[0]: self.show_edit_dialog(id))
            self.wishlist_table.setCellWidget(row, 4, edit_button)

            delete_button = QPushButton("Hapus")
            delete_button.setObjectName("wishlist_button")
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
        status_input.addItems(["Belum Terpenuhi", "Sudah Terpenuhi"])
        current_status = "Sudah Terpenuhi" if wishlist[3] == "true" else "Belum Terpenuhi"
        status_input.setCurrentText(current_status)
        layout.addWidget(status_label)
        layout.addWidget(status_input)

        # Tombol Simpan
        save_button = QPushButton("Simpan")
        save_button.clicked.connect(lambda: self.save_edit(dialog, wishlist_id, name_input.text(), price_input.value(), 
                                                         "true" if status_input.currentText() == "Sudah Terpenuhi" else "false"))
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