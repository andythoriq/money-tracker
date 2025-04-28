from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QGroupBox, QSpinBox, QMessageBox, QInputDialog, QSizePolicy
)
from controller.Popup import PopupWarning, PopupSuccess
from controller.wallet import Wallet

class WalletView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        # Main layout
        self.setMinimumSize(700, 600)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        title_label = QLabel("Wallet")
        title_label.setObjectName("tittleLabel")
        main_layout.addWidget(title_label)

        # Content Container
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # === BOX TAMBAH WALLET ===
        self.group_add_wallet = QGroupBox("Tambah Wallet")
        self.group_add_wallet.setObjectName("groupBox")
        self.group_add_wallet.setStyleSheet("""
            QGroupBox {
                color: white;
                font-size: 14px;
                padding: 15px;
                border: none;
            }
        """)
        layout_add_wallet = QHBoxLayout()
        layout_add_wallet.setSpacing(10)

        # Labels
        name_label = QLabel("Nama:")
        name_label.setStyleSheet("background-color:  #7A9F60; color: white; font-size: 14px; padding: 5px; border-radius: 5px;")
        saldo_label = QLabel("Saldo:")
        saldo_label.setStyleSheet("background-color: #7A9F60; color: white; font-size: 14px; padding: 5px; border-radius: 5px;")

        # Input fields
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nama Wallet")
        self.input_name.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        self.input_amount = QSpinBox()
        self.input_amount.setMinimum(0)
        self.input_amount.setMaximum(1000000000)
        self.input_amount.setPrefix("Rp ")
        self.input_amount.setSingleStep(50000)
        self.input_amount.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        self.btn_add = QPushButton("Tambah")
        self.btn_add.setStyleSheet("""
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
        self.btn_add.clicked.connect(self.add_wallet)

        layout_add_wallet.addWidget(name_label)
        layout_add_wallet.addWidget(self.input_name)
        layout_add_wallet.addWidget(saldo_label)
        layout_add_wallet.addWidget(self.input_amount)
        layout_add_wallet.addWidget(self.btn_add)

        self.group_add_wallet.setLayout(layout_add_wallet)
        content_layout.addWidget(self.group_add_wallet)

        # === TABEL WALLET ===
        self.table_wallet = QTableWidget()
        self.table_wallet.setObjectName("tableWallet")
        self.table_wallet.setColumnCount(4)
        self.table_wallet.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_wallet.setHorizontalHeaderLabels(["Nama", "Saldo", "Edit", "Delete"])
        self.table_wallet.setStyleSheet("""
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
        self.table_wallet.horizontalHeader().setStretchLastSection(False)
        self.table_wallet.setColumnWidth(0, 200)  # Nama column
        self.table_wallet.setColumnWidth(1, 200)  # Saldo column
        self.table_wallet.setColumnWidth(2, 100)  # Edit column
        self.table_wallet.setColumnWidth(3, 100)  # Delete column
        
        self.table_wallet.verticalHeader().setVisible(False)
        content_layout.addWidget(self.table_wallet)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_wallets()
        # Set stylesheet for the main widget
        self.setStyleSheet("background-color: #98C379;")

    def load_wallets(self):
        """Memuat data wallet ke tabel"""
        wallets = self.wallet_controller.load_wallets()
        self.table_wallet.setRowCount(len(wallets))

        for row, wallet in enumerate(wallets):
            name_item = QTableWidgetItem(wallet.get("name"))
            amount_item = QTableWidgetItem(f"Rp {wallet.get('amount')}")

            btn_edit = QPushButton("Edit")
            btn_edit.setFixedWidth(80)
            btn_edit.setStyleSheet("""
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
            btn_edit.clicked.connect(lambda _, n=wallet.get("name"): self.edit_wallet(n))

            btn_delete = QPushButton("Hapus")
            btn_delete.setFixedWidth(80)
            btn_delete.setStyleSheet("""
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
            btn_delete.clicked.connect(lambda _, n=wallet.get("name"): self.delete_wallet(n))

            self.table_wallet.setItem(row, 0, name_item)
            self.table_wallet.setItem(row, 1, amount_item)
            self.table_wallet.setCellWidget(row, 2, btn_edit)
            self.table_wallet.setCellWidget(row, 3, btn_delete)

    def add_wallet(self):
        """Menambah wallet baru"""
        name = self.input_name.text().strip()
        amount = self.input_amount.value()

        
        result = self.wallet_controller.add_wallet(name, amount)
        if result.get("valid"):
            self.load_wallets()
            self.input_name.clear()
            self.input_amount.setValue(0)
            PopupSuccess("Success", "Pemasukkan berhasil disimpan!")
        else:
            errors = result.get("errors")
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            PopupWarning("Warning", f"Gagal menyimpan pemasukkan!\n{error_message}")

    def edit_wallet(self, name):
        """Mengedit saldo wallet"""
        dialog = QInputDialog(self)
        dialog.setObjectName("label")
        new_amount, ok = dialog.getInt(self, "Edit Wallet", f"Saldo baru untuk {name}:", min=0)
        if ok:
            result = self.wallet_controller.edit_wallet(name, new_amount)
            if result.get("valid"):
                self.load_wallets()
                PopupSuccess("Success", "Wallet berhasil disimpan!")
            else:
                errors = result.get("errors")
                error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
                PopupWarning("Warning", f"Gagal menyimpan wallet!\n{error_message}")

    def delete_wallet(self, name):
        """Menghapus wallet"""
        msg = QMessageBox()
        msg.setObjectName("deleteWallet")
        msg.setWindowTitle("Konfirmasi")
        msg.setText(f"Apakah Anda yakin ingin menghapus wallet '{name}'?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #98C379;
                padding: 5px;
            }
            QLabel {
                background-color: #7A9F60;
                padding: 8px;
                border-radius: 5px;
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
        
        result = msg.exec_()
        if result == QMessageBox.Yes:
            self.wallet_controller.delete_wallet(name)
            self.load_wallets()
