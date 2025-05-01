from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QGroupBox, QSpinBox, QMessageBox, QInputDialog, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt, QCoreApplication
from controller.wallet import Wallet

class WalletView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        self.title_label = QLabel("Wallet")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

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
        self.name_label = QLabel("Nama:")
        self.name_label.setObjectName("form_label")
        self.saldo_label = QLabel("Saldo:")
        self.saldo_label.setObjectName("form_label")

        # Input fields
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Nama Wallet")
        self.input_name.setObjectName("wishlist_input")

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
        self.btn_add.setObjectName("add_button")
        self.btn_add.clicked.connect(self.add_wallet)

        layout_add_wallet.addWidget(self.name_label)
        layout_add_wallet.addWidget(self.input_name)
        layout_add_wallet.addWidget(self.saldo_label)
        layout_add_wallet.addWidget(self.input_amount)
        layout_add_wallet.addWidget(self.btn_add)

        self.group_add_wallet.setLayout(layout_add_wallet)
        content_layout.addWidget(self.group_add_wallet)

        # === TABEL WALLET ===
        self.table_wallet = QTableWidget()
        self.table_wallet.setObjectName("table")
        self.table_wallet.setColumnCount(4)
        self.table_wallet.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_wallet.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_wallet.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_wallet.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_wallet.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_wallet.setHorizontalHeaderLabels(["Nama", "Saldo", "Edit", "Delete"])

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

    def load_wallets(self):
        """Memuat data wallet ke tabel"""
        wallets = self.wallet_controller.load_wallets()
        self.table_wallet.setRowCount(len(wallets))

        for row, wallet in enumerate(wallets):
            name_item = QTableWidgetItem(wallet[0])
            amount_item = QTableWidgetItem(f"Rp {wallet[1]}")

            self.btn_edit = QPushButton("Edit")
            self.btn_edit.setFixedWidth(80)
            self.btn_edit.setObjectName("Edit")
            self.btn_edit.clicked.connect(lambda _, n=wallet[0]: self.edit_wallet(n))

            self.btn_delete = QPushButton("Hapus")
            self.btn_delete.setFixedWidth(80)
            self.btn_delete.setObjectName("Delete")
            self.btn_delete.clicked.connect(lambda _, n=wallet[0]: self.delete_wallet(n))

            self.table_wallet.setItem(row, 0, name_item)
            self.table_wallet.setItem(row, 1, amount_item)
            self.table_wallet.setCellWidget(row, 2, self.btn_edit)
            self.table_wallet.setCellWidget(row, 3, self.btn_delete)

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
            msg = QMessageBox()
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #7A9F60;
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
            msg.setText("Nama wallet tidak boleh kosong!")
            msg.exec_()

    def edit_wallet(self, name):
        """Mengedit saldo wallet"""
        dialog = QInputDialog(self)
        dialog.setObjectName("label")
        new_amount, ok = dialog.getInt(self, "Edit Wallet", f"Saldo baru untuk {name}:", min=0)
        if ok:
            self.wallet_controller.edit_wallet(name, new_amount)
            self.load_wallets()

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

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("wallet", {}).get("Title", "")))
            self.name_label.setText(_translate("Form", lang.get("wallet", {}).get("form1", "") + ":"))
            self.saldo_label.setText(_translate("Form", lang.get("wallet", {}).get("form2", "") + ":"))
            self.btn_add.setText(_translate("Form", lang.get("wallet", {}).get("btn", "")))
            self.input_name.setPlaceholderText(_translate("Form", lang.get("wallet", {}).get("desc1", "")))
            self.group_add_wallet.setTitle(_translate("Form", lang.get("wallet", {}).get("entry", "")))
            self.table_wallet.setHorizontalHeaderLabels(
                [
                    lang.get("wallet", {}).get("col1", ""), 
                    lang.get("wallet", {}).get("col2", ""), 
                    lang.get("wallet", {}).get("col3", ""), 
                    lang.get("wallet", {}).get("col4", "")
                    ]
                )
            self.btn_edit.setText(_translate("Form", lang.get("wallet", {}).get("col3", "")))
            self.btn_delete.setText(_translate("Form", lang.get("wallet", {}).get("col4", "")))
