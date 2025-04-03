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
        self.setObjectName("HomeSection")

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        title_label = QLabel("Wishlist")
        title_label.setObjectName("Label_1")
        main_layout.addWidget(title_label)

        # Content Container
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # === Form Tambah Wishlist ===
        form_widget = QWidget()
        form_widget.setObjectName("groupBox")
        form_layout = QHBoxLayout(form_widget)
        form_layout.setSpacing(10)

        # Labels with white text
        name_label = QLabel("Nama:")
        name_label.setStyleSheet("color: white; font-size: 14px;")
        price_label = QLabel("Harga:")
        price_label.setStyleSheet("color: white; font-size: 14px;")

        # Input fields
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        self.price_input = QSpinBox()
        self.price_input.setRange(1, 10_000_000)
        self.price_input.setSingleStep(50_000)
        self.price_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        add_button = QPushButton("Tambah Wishlist")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        add_button.clicked.connect(self.add_wishlist)

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(price_label)
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(add_button)

        content_layout.addWidget(form_widget)

        # === Filter Berdasarkan Status ===
        filter_widget = QWidget()
        filter_widget.setObjectName("groupBox")
        status_layout = QHBoxLayout(filter_widget)
        status_layout.setSpacing(10)

        filter_label = QLabel("Filter Status:")
        filter_label.setStyleSheet("color: white; font-size: 14px;")
        status_layout.addWidget(filter_label)

        self.all_status = QRadioButton("Semua")
        self.unfulfilled_status = QRadioButton("Belum Terpenuhi")
        self.fulfilled_status = QRadioButton("Sudah Terpenuhi")

        for radio in [self.all_status, self.unfulfilled_status, self.fulfilled_status]:
            radio.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 14px;
                    padding: 5px;
                }
                QRadioButton::indicator {
                    width: 15px;
                    height: 15px;
                }
            """)

        self.all_status.setChecked(True)

        status_layout.addWidget(self.all_status)
        status_layout.addWidget(self.unfulfilled_status)
        status_layout.addWidget(self.fulfilled_status)
        status_layout.addStretch()

        self.all_status.toggled.connect(self.load_wishlists)
        self.unfulfilled_status.toggled.connect(self.load_wishlists)
        self.fulfilled_status.toggled.connect(self.load_wishlists)

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
        content_layout.addWidget(filter_widget)

        # === Tabel Wishlist ===
        self.wishlist_table = QTableWidget()
        self.wishlist_table.setObjectName("table")
        self.wishlist_table.setColumnCount(6)
        self.wishlist_table.setHorizontalHeaderLabels(["ID", "Nama", "Harga", "Status", "Edit", "Delete"])
        self.wishlist_table.setStyleSheet("""
            QTableWidget {
                background-color: #7A9F60;
                border-radius: 10px;
                color: white;
                gridline-color: #98C379;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #6A8B52;
            }
            QHeaderView::section {
                background-color: #7A9F60;
                color: white;
                padding: 5px;
                border: none;
            }
            QScrollBar {
                background-color: #7A9F60;
            }
        """)
        
        # Set column widths
        self.wishlist_table.horizontalHeader().setStretchLastSection(False)
        self.wishlist_table.setColumnWidth(0, 50)   # ID column
        self.wishlist_table.setColumnWidth(1, 200)  # Nama column
        self.wishlist_table.setColumnWidth(2, 150)  # Harga column
        self.wishlist_table.setColumnWidth(3, 150)  # Status column
        self.wishlist_table.setColumnWidth(4, 100)  # Edit column
        self.wishlist_table.setColumnWidth(5, 100)  # Delete column
        
        self.wishlist_table.verticalHeader().setVisible(False)
        content_layout.addWidget(self.wishlist_table)

        # === Tombol Kembali ===
        self.btn_back = QPushButton("Kembali ke Dashboard")
        self.btn_back.setObjectName("btn_home")
        self.btn_back.clicked.connect(self.go_back)
        content_layout.addWidget(self.btn_back)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_wishlists()

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
            edit_button.setFixedWidth(80)
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            edit_button.clicked.connect(lambda _, id=wishlist[0]: self.show_edit_dialog(id))
            self.wishlist_table.setCellWidget(row, 4, edit_button)

            delete_button = QPushButton("Hapus")
            delete_button.setFixedWidth(80)
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            delete_button.clicked.connect(lambda _, id=wishlist[0], name=wishlist[1], price=wishlist[2]: self.delete_wishlist(id, name, price))
            self.wishlist_table.setCellWidget(row, 5, delete_button)

    def add_wishlist(self):
        """Menambahkan wishlist baru"""
        name = self.name_input.text().strip()
        price = self.price_input.value()

        if not name:
            msg = QMessageBox()
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            msg.setWindowTitle("Error")
            msg.setText("Nama tidak boleh kosong!")
            msg.exec_()
            return

        self.wishlist_controller.add_wishlist(name, price, False)
        
        success_msg = QMessageBox()
        success_msg.setStyleSheet("""
            QMessageBox {
                background-color: #98C379;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        success_msg.setWindowTitle("Sukses")
        success_msg.setText("Wishlist berhasil ditambahkan!")
        success_msg.exec_()

        self.load_wishlists()
        self.name_input.clear()
        self.price_input.setValue(1)

    def show_edit_dialog(self, wishlist_id):
        """Menampilkan popup edit wishlist"""
        wishlist = next((w for w in self.wishlist_controller.wishlists if w[0] == wishlist_id), None)
        if not wishlist:
            msg = QMessageBox()
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            msg.setWindowTitle("Error")
            msg.setText("Wishlist tidak ditemukan!")
            msg.exec_()
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Wishlist")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #98C379;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

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
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_button.clicked.connect(lambda: self.save_edit(dialog, wishlist_id, name_input.text(), price_input.value(), status_input.currentText()))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edit(self, dialog, wishlist_id, name, price, status):
        """Menyimpan hasil edit wishlist"""
        if not name:
            msg = QMessageBox()
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            msg.setWindowTitle("Error")
            msg.setText("Nama tidak boleh kosong!")
            msg.exec_()
            return

        success = self.wishlist_controller.edit_wishlist(wishlist_id, name, price, status)
        if success:
            success_msg = QMessageBox()
            success_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            success_msg.setWindowTitle("Sukses")
            success_msg.setText("Wishlist berhasil diperbarui!")
            success_msg.exec_()
            self.load_wishlists()
            dialog.accept()
        else:
            error_msg = QMessageBox()
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            error_msg.setWindowTitle("Error")
            error_msg.setText("Gagal mengupdate wishlist!")
            error_msg.exec_()

    def delete_wishlist(self, wishlist_id, name, price):
        """Konfirmasi dan hapus wishlist"""
        msg = QMessageBox()
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #98C379;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.setWindowTitle("Hapus Wishlist")
        msg.setText(f"Apakah Anda ingin menghapus {name} yang bernilai {price}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        result = msg.exec_()
        if result == QMessageBox.Yes:
            success = self.wishlist_controller.delete_wishlist(wishlist_id)
            if success:
                success_msg = QMessageBox()
                success_msg.setStyleSheet(msg.styleSheet())
                success_msg.setWindowTitle("Sukses")
                success_msg.setText("Wishlist berhasil dihapus!")
                success_msg.exec_()
                self.load_wishlists()
            else:
                error_msg = QMessageBox()
                error_msg.setStyleSheet(msg.styleSheet())
                error_msg.setWindowTitle("Error")
                error_msg.setText("Gagal menghapus wishlist!")
                error_msg.exec_()

    def go_back(self):
        self.parent().setCurrentIndex(0)