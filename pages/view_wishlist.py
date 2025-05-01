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
        form_layout.addWidget(self.price_input)

        # Add button
        self.add_button = QPushButton("Tambah Wishlist")
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_wishlist)
        form_layout.addWidget(self.add_button)

        form_layout.addStretch()
        
        # Filter status layout
        status_widget = QWidget()
        status_widget.setObjectName("groupBox")
        status_layout = QHBoxLayout(status_widget)
        status_layout.setSpacing(15)
        
        self.filter_label = QLabel("Filter Status:")
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
            self.edit_button = QPushButton("Edit")
            self.edit_button.setFixedWidth(80)
            self.edit_button.setObjectName("Edit")
            self.edit_button.clicked.connect(lambda _, id=wishlist[0]: self.show_edit_dialog(id))
            self.wishlist_table.setCellWidget(row, 4, self.edit_button)

            self.delete_button = QPushButton("Hapus")
            self.delete_button.setFixedWidth(80)
            self.delete_button.setObjectName("Delete")
            self.delete_button.clicked.connect(lambda _, id=wishlist[0], name=wishlist[1], price=wishlist[2]: self.delete_wishlist(id, name, price))
            self.wishlist_table.setCellWidget(row, 5, self.delete_button)

    def add_wishlist(self):
        """Menambahkan wishlist baru"""
        name = self.name_input.text().strip()
        price = self.price_input.value()

        result = self.wishlist_controller.add_wishlist(name, price, False)  # Status default False
        
        if result.get("valid"):
            self.load_wishlists()  # Muat ulang daftar wishlist
            self.name_input.clear()
            self.price_input.setValue(1)
            PopupSuccess("Success", "Wishlist berhasil disimpan!")
        else:
            errors = result.get("errors")
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            PopupWarning("Warning", f"Gagal menyimpan wishlist!\n{error_message}")

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

        result = self.wishlist_controller.edit_wishlist(wishlist_id, name, price, status)
        if result.get('valid'):
            self.load_wishlists()
            PopupSuccess("Success", "Wishlist berhasil disimpan!")
        else:
            errors = result.get("errors")
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            PopupWarning("Warning", f"Gagal menyimpan wishlist!\n{error_message}")

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

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("wishlist", {}).get("Title", "")))
            self.name_label.setText(_translate("Form", lang.get("wishlist", {}).get("form1", "") + ":"))
            self.price_label.setText(_translate("Form", lang.get("wishlist", {}).get("form2", "") + ":"))
            self.add_button.setText(_translate("Form", lang.get("wishlist", {}).get("btn1", "")))
            self.filter_label.setText(_translate("Form", lang.get("wishlist", {}).get("filter", "") + ":"))
            self.all_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn1", "")))
            self.fulfilled_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn2", "")))
            self.unfulfilled_status.setText(_translate("Form", lang.get("wishlist", {}).get("radbtn3", "")))
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