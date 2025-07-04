from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QGroupBox, QSpinBox, QMessageBox, QInputDialog, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import Qt, QCoreApplication
from controller.Popup import PopupWarning, PopupSuccess
from controller.wallet import Wallet
from components.MoneyLineEdit import MoneyLineEdit
from utils.number_formatter import NumberFormat

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
        self.group_add_wallet = QGroupBox("")
        self.group_add_wallet.setObjectName("walletcontent")
        self.group_add_wallet.setStyleSheet("""
            QGroupBox {
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
        self.input_amount = MoneyLineEdit(locale_str='id_ID')

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
            name_item = QTableWidgetItem(wallet.get("name"))
            amount_item = QTableWidgetItem(f"Rp {NumberFormat.getFormattedMoney(wallet.get('amount'))}")

            self.btn_edit = QPushButton()
            self.btn_edit.setFixedWidth(80)
            self.btn_edit.setObjectName("Edit")
            self.btn_edit.clicked.connect(
                lambda _, n=wallet.get("name"), a=wallet.get("amount"): self.edit_wallet(n, a)
            )

            self.btn_delete = QPushButton()
            self.btn_delete.setFixedWidth(80)
            self.btn_delete.setObjectName("Delete")
            self.btn_delete.clicked.connect(lambda _, n=wallet.get("name"): self.delete_wallet(n))

            self.table_wallet.setItem(row, 0, name_item)
            self.table_wallet.setItem(row, 1, amount_item)
            self.table_wallet.setCellWidget(row, 2, self.btn_edit)
            self.table_wallet.setCellWidget(row, 3, self.btn_delete)

    def add_wallet(self):
        """Menambah wallet baru"""
        name = self.input_name.text().strip()
        amount = self.input_amount.get_value()

        if name:
            self.wallet_controller.add_wallet(name, amount)
            self.load_wallets()
            self.input_name.clear()
            self.input_amount.set_value(0)
        else:
            msg = QMessageBox()

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
        msg.setStyleSheet("""  
         QPushButton {
                background-color: #000000;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 70px;
            }""")
        msg.setObjectName("deleteWallet")
        msg.setWindowTitle("Konfirmasi")
        msg.setText(f"Apakah Anda yakin ingin menghapus wallet '{name}'?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
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
            self.table_wallet.setHorizontalHeaderLabels(
                [
                    lang.get("wallet", {}).get("col1", ""), 
                    lang.get("wallet", {}).get("col2", ""), 
                    lang.get("wallet", {}).get("col3", ""), 
                    lang.get("wallet", {}).get("col4", "")
                    ]
                )
            for row in range(self.table_wallet.rowCount()):
                widget = self.table_wallet.cellWidget(row, 2)
                if isinstance(widget, QPushButton):
                    widget.setText(_translate("Form", lang.get("wallet", {}).get("col3", "")))
            for row in range(self.table_wallet.rowCount()):
                widget = self.table_wallet.cellWidget(row, 3)
                if isinstance(widget, QPushButton):
                    widget.setText(_translate("Form", lang.get("wallet", {}).get("col4", "")))


