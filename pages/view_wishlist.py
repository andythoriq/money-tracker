import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QRadioButton, QLineEdit, QMessageBox, QSpinBox, QComboBox, QLabel, QDialog, 
    QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, QCoreApplication
from controller.Popup import PopupWarning, PopupSuccess
from controller.wishlist import Wishlist
from controller.wallet import Wallet

class WishlistView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.wishlist_controller = Wishlist(Wallet())
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        # Main container with dark background
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        self.title_label = QLabel("Wishlist")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

        # Content container with green background
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Form layout
        form_widget = QWidget()
        form_widget.setObjectName("groupBox")
        form_layout = QHBoxLayout(form_widget)
        form_layout.setSpacing(15)

        # Name input
        self.name_label = QLabel("Nama:")
        self.name_label.setObjectName("form_label")
        form_layout.addWidget(self.name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setObjectName("wishlist_input")
        self.name_input.setPlaceholderText("Nama Target")
        self.name_input.setFixedWidth(400)
        form_layout.addWidget(self.name_input)

        # Price input
        self.price_label = QLabel("Harga:")
        self.price_label.setObjectName("form_label")
        form_layout.addWidget(self.price_label)
        
        self.price_input = QSpinBox()
        self.price_input.setObjectName("wishlist_input")
        self.price_input.setRange(0, 100_000_000)
        self.price_input.setSingleStep(50_000)
        self.price_input.setPrefix("Rp ")
        self.price_input.setFixedWidth(200)
        form_layout.addWidget(self.price_input)

        # Add button
        self.add_button = QPushButton("Tambah Wishlist")
        self.add_button.setObjectName("add_button")
        self.add_button.setFixedWidth(175)
        self.add_button.clicked.connect(self.add_wishlist)
        form_layout.addWidget(self.add_button)

        form_layout.addStretch()
        
        # Filter status layout
        status_widget = QWidget()
        status_widget.setObjectName("groupBox")
        status_layout = QHBoxLayout(status_widget)
        status_layout.setSpacing(15)
        
        self.filter_label = QLabel("Filter by Status:")
        self.filter_label.setObjectName("form_label")
        status_layout.addWidget(self.filter_label)

        # Radio buttons
        self.all_status = QRadioButton("Semua")
        self.unfulfilled_status = QRadioButton("Belum Terpenuhi")
        self.fulfilled_status = QRadioButton("Sudah Terpenuhi")

        for radio in [self.all_status, self.unfulfilled_status, self.fulfilled_status]:
            radio.setObjectName("wishlist_radio")
            status_layout.addWidget(radio)

        self.all_status.setChecked(True)

        # Wallet filter 
        self.wallet_filter_label = QLabel("Filter by Wallet:")
        self.wallet_filter_label.setObjectName("form_label")
        status_layout.addWidget(self.wallet_filter_label)
        self.wallet_filter_combo = QComboBox()
        self.wallet_filter_combo.setObjectName("wallet_filter_combo")
        self.wallet_filter_combo.addItem("Semua Wallet")
        for name in self.wallet_controller.get_wallet_name():
            self.wallet_filter_combo.addItem(name)
        self.wallet_filter_combo.currentIndexChanged.connect(self.load_wishlists)
        status_layout.addWidget(self.wallet_filter_combo)

        status_layout.addStretch()

        self.all_status.toggled.connect(self.load_wishlists)
        self.unfulfilled_status.toggled.connect(self.load_wishlists)
        self.fulfilled_status.toggled.connect(self.load_wishlists)

        # Table
        self.wishlist_table = QTableWidget()
        self.wishlist_table.setObjectName("table")
        self.wishlist_table.setColumnCount(6)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.wishlist_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        # self.wishlist_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.wishlist_table.setHorizontalHeaderLabels(["No.", "Nama", "Harga", "Status", "Edit", "Delete"])
        
        # Adjust column widths proportionally
        total_width = self.wishlist_table.viewport().width()
        self.wishlist_table.setColumnWidth(0, int(total_width * 0.02))  # 5% for No.
        self.wishlist_table.setColumnWidth(1, int(total_width * 0.37))  # 35% for Nama
        self.wishlist_table.setColumnWidth(2, int(total_width * 0.20))  # 20% for Harga
        self.wishlist_table.setColumnWidth(3, int(total_width * 0.20))  # 20% for Status
        self.wishlist_table.setColumnWidth(4, int(total_width * 0.10))  # 10% for Edit
        self.wishlist_table.setColumnWidth(5, int(total_width * 0.10))  # 10% for Delete

        self.wishlist_table.verticalHeader().setVisible(False)
        self.wishlist_table.setMinimumHeight(300)  # Set minimum height for table
        self.load_wishlists()

        content_layout.addWidget(form_widget)
        content_layout.addWidget(status_widget)
        content_layout.addWidget(self.wishlist_table)

        # Add content to main layout
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)

    def load_wishlists(self):
        """Memuat data wishlist ke tabel berdasarkan filter"""
        # Filter by wallet
        selected_wallet = self.wallet_filter_combo.currentText() if hasattr(self, 'wallet_filter_combo') else None
        if selected_wallet and selected_wallet != "Semua Wallet":
            wishlists = self.wishlist_controller.filter_by_wallet(selected_wallet)
        else:
            wishlists = self.wishlist_controller.wishlists

        # Filter status
        if self.unfulfilled_status.isChecked():
            wishlists = [w for w in wishlists if not w.get("status")]
        elif self.fulfilled_status.isChecked():
            wishlists = [w for w in wishlists if w.get("status")]

        # Muat data ke tabel
        self.wishlist_table.setRowCount(len(wishlists))
        for row, wishlist in enumerate(wishlists):
            if len(wishlist) < 4:
                continue
            self.wishlist_table.setItem(row, 0, QTableWidgetItem(str(wishlist.get("ID"))))    # ID
            self.wishlist_table.setItem(row, 1, QTableWidgetItem(wishlist.get("label")))  # Nama
            self.wishlist_table.setItem(row, 2, QTableWidgetItem(f"Rp {wishlist.get('price')}")) # Harga
            status_text = "Sudah Terpenuhi" if wishlist.get("status") else "Belum Terpenuhi"
            self.wishlist_table.setItem(row, 3, QTableWidgetItem(status_text))  # Status
            edit_button = QPushButton("Edit")
            edit_button.setObjectName("Edit")
            edit_button.clicked.connect(lambda _, id=wishlist.get("ID"): self.show_edit_dialog(id))
            self.wishlist_table.setCellWidget(row, 4, edit_button)
            delete_button = QPushButton("Hapus")
            delete_button.setObjectName("Delete")
            delete_button.clicked.connect(lambda _, id=wishlist.get("ID"), name=wishlist.get("label"), price=wishlist.get("price"): self.delete_wishlist(id, name, price))
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
        wishlist = next((w for w in self.wishlist_controller.wishlists if w.get("ID") == wishlist_id), None)
        if not wishlist:
            QMessageBox.warning(self, "Error", "Wishlist tidak ditemukan!")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Wishlist")
        layout = QVBoxLayout()

        # Nama
        name_label = QLabel("Nama:")
        name_input = QLineEdit()
        name_input.setText(wishlist.get("label"))
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        # Harga
        price_label = QLabel("Harga:")
        price_input = QSpinBox()
        price_input.setRange(1, 10_000_000)
        price_input.setSingleStep(50_000)
        price_input.setValue(int(wishlist.get("price")))
        layout.addWidget(price_label)
        layout.addWidget(price_input)

        # Status
        status_label = QLabel("Status:")
        status_input = QComboBox()
        status_input.addItems(["Belum Terpenuhi", "Sudah Terpenuhi"])
        current_status = "Sudah Terpenuhi" if wishlist.get("status") else "Belum Terpenuhi"
        status_input.setCurrentText(current_status)
        layout.addWidget(status_label)
        layout.addWidget(status_input)

        # Tombol Simpan
        save_button = QPushButton("Simpan")
        save_button.clicked.connect(lambda: self.save_edit(dialog, wishlist_id, name_input.text(), price_input.value(), 
                                                         True if status_input.currentText() == "Sudah Terpenuhi" else False))
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

    def delete_wishlist(self, wishlist_id, label, price):
        """Konfirmasi dan hapus wishlist"""
        confirm = QMessageBox.question(self, "Hapus Wishlist", f"Apakah Anda ingin menghapus {label} yang bernilai {price}?", 
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

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("wishlist", {}).get("Title", "")))
            self.name_label.setText(_translate("Form", lang.get("wishlist", {}).get("form1", "") + ":"))
            self.name_input.setPlaceholderText(_translate("Form", lang.get("wishlist", {}).get("Placeholder", "")))
            self.price_label.setText(_translate("Form", lang.get("wishlist", {}).get("form2", "") + ":"))
            self.add_button.setText(_translate("Form", lang.get("wishlist", {}).get("btn1", "")))
            self.filter_label.setText(_translate("Form", lang.get("wishlist", {}).get("filter", "") + ":"))
            self.all_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn1", "")))
            self.fulfilled_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn2", "")))
            self.unfulfilled_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn3", "")))
            self.wallet_filter_label.setText(_translate("Form", lang.get("wishlist", {}).get("wallet_filter", "")))
            self.wallet_filter_combo.clear()
            self.wallet_filter_combo.addItem("Semua Wallet")
            for name in self.wallet_controller.get_wallet_name():
                self.wallet_filter_combo.addItem(name)
            self.wishlist_table.setHorizontalHeaderLabels(               
                [
                    lang.get("wishlist", {}).get("col1", ""), 
                    lang.get("wishlist", {}).get("col2", ""), 
                    lang.get("wishlist", {}).get("col3", ""), 
                    lang.get("wishlist", {}).get("col4", ""), 
                    lang.get("wishlist", {}).get("col5", ""), 
                    lang.get("wishlist", {}).get("col6", ""), 
                    ]
                )