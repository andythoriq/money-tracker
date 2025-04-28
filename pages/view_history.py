from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QLabel, QRadioButton, 
    QButtonGroup, QDialog, QFormLayout, QSpinBox, 
    QComboBox, QLineEdit, QCalendarWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from datetime import datetime
from controller.income import Income
from controller.outcome import Outcome
from controller.wallet import Wallet
from controller.category import Category
from controller.Popup import PopupWarning, PopupSuccess

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.category_controller = Category()
        self.income_controller = Income(self.wallet_controller)
        self.outcome_controller = Outcome(self.wallet_controller)
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        """Inisialisasi UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        title_label = QLabel("History")
        title_label.setObjectName("tittleLabel")
        main_layout.addWidget(title_label)

        # Content Container
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Radio Button Filter
        filter_widget = QWidget()
        filter_widget.setObjectName("groupBox")
        btn_layout = QHBoxLayout(filter_widget)
        btn_layout.setSpacing(10)
        self.radio_group = QButtonGroup(self)

        self.radio_all = QRadioButton("Semua")
        self.radio_all.setObjectName("btn_home")
        self.radio_income = QRadioButton("Income")
        self.radio_income.setObjectName("btn_home")
        self.radio_outcome = QRadioButton("Outcome")
        self.radio_outcome.setObjectName("btn_home")

        for radio in [self.radio_all, self.radio_income, self.radio_outcome]:
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

        self.radio_group.addButton(self.radio_all)
        self.radio_group.addButton(self.radio_income)
        self.radio_group.addButton(self.radio_outcome)

        self.radio_all.setChecked(True)
        self.radio_income.toggled.connect(lambda: self.load_data("income"))
        self.radio_outcome.toggled.connect(lambda: self.load_data("outcome"))
        self.radio_all.toggled.connect(lambda: self.load_data("all"))

        btn_layout.addWidget(self.radio_all)
        btn_layout.addWidget(self.radio_income)
        btn_layout.addWidget(self.radio_outcome)
        btn_layout.addStretch()
        content_layout.addWidget(filter_widget)

        # Tabel Transaksi
        self.table = QTableWidget()
        self.table.setObjectName("table")
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Jumlah", "Kategori", "Dompet", "Deskripsi", "Edit", "Delete"])
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
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
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        content_layout.addWidget(self.table)
        self.setStyleSheet("background-color: #98C379;")

        # Label Total
        self.label = QLabel("Total : Rp 0")
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignRight)
        content_layout.addWidget(self.label)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_data("all")

    def load_data(self, filter_type):
        """Memuat data ke tabel berdasarkan filter"""
        self.table.setRowCount(0)
        transactions = []
        total = 0

        # Load data income
        for income in self.income_controller.load_incomes():
            transactions.append({
                "id": income.get("ID"),
                "date": datetime.strptime(income.get("date"), "%d/%m/%Y"),
                "type": "income",
                "amount": income.get("amount"),
                "category": income.get("category"),
                "wallet": income.get("wallet"),
                "desc": income.get("desc")
            })

        # Load data outcome
        for outcome in self.outcome_controller.load_outcomes():
            transactions.append({
                "id": outcome.get("ID"),
                "date": datetime.strptime(outcome.get("date"), "%d/%m/%Y"),
                "type": "outcome",
                "amount": outcome.get("amount"),
                "category": outcome.get("category"),
                "wallet": outcome.get("wallet"),
                "desc": outcome.get("desc")
            })

        # Filter transaksi
        if self.radio_all.isChecked():
            transactions = [t for t in transactions]
        elif filter_type == "income":
            transactions = [t for t in transactions if t["type"] == "income"]
        elif filter_type == "outcome":
            transactions = [t for t in transactions if t["type"] == "outcome"]

        transactions.sort(key=lambda x: x["date"], reverse=True)

        # Tampilkan data di tabel
        self.table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            if transaction["type"] == "income":
                total += int(transaction["amount"])
            else:
                total -= int(transaction["amount"])

            self.table.setItem(row, 0, QTableWidgetItem(transaction["date"].strftime("%d/%m/%Y")))
            self.table.setItem(row, 1, QTableWidgetItem(transaction["type"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"Rp {transaction['amount']}"))
            self.table.setItem(row, 3, QTableWidgetItem(transaction["category"]))
            self.table.setItem(row, 4, QTableWidgetItem(transaction["wallet"]))
            self.table.setItem(row, 5, QTableWidgetItem(transaction["desc"]))

            # Tombol Edit
            btn_edit = QPushButton("Edit")
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
            btn_edit.clicked.connect(lambda _, t=transaction: self.open_edit_popup(t))
            self.table.setCellWidget(row, 6, btn_edit)

            # Tombol Delete
            btn_delete = QPushButton("Delete")
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
            btn_delete.clicked.connect(lambda _, t=transaction: self.confirm_delete(t))
            self.table.setCellWidget(row, 7, btn_delete)

        self.label.setText(f"Total : Rp {total}")

    def open_edit_popup(self, transaction):
        """Popup Edit Data"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Transaksi")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #98C379;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QSpinBox, QComboBox, QLineEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
            }
            QCalendarWidget {
                background-color: white;
                border-radius: 5px;
            }
        """)
        layout = QFormLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Widget Form
        amount_input = QSpinBox()
        amount_input.setMaximum(100000000)
        amount_input.setValue(int(transaction["amount"]))

        category_input = QComboBox()
        category_input.addItems(self.category_controller.load_category_names(transaction["type"]))
        category_input.setCurrentText(transaction["category"])

        wallet_input = QComboBox()
        wallet_input.addItems(self.wallet_controller.get_wallet_name())
        wallet_input.setCurrentText(transaction["wallet"])

        desc_input = QLineEdit(transaction["desc"])

        date_input = QCalendarWidget()
        date_input.setSelectedDate(transaction["date"])

        layout.addRow("Jumlah:", amount_input)
        layout.addRow("Kategori:", category_input)
        layout.addRow("Dompet:", wallet_input)
        layout.addRow("Deskripsi:", desc_input)
        layout.addRow("Tanggal:", date_input)

        # Tombol Simpan
        btn_save = QPushButton("Simpan")
        btn_save.setStyleSheet("""
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
        btn_save.clicked.connect(lambda: self.save_edit(transaction, amount_input, category_input, wallet_input, desc_input, date_input, dialog))
        layout.addRow(btn_save)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edit(self, transaction, amount, category, wallet, desc, date, dialog):
        """Simpan perubahan edit transaksi"""
        new_data = {
            "ID": transaction["id"],
            "amount": amount.value(),
            "category": category.currentText(),
            "wallet": wallet.currentText(),
            "desc": desc.text(),
            "date": date.selectedDate().toString("dd/MM/yyyy")
        }

        if transaction["type"] == "income":
            result = self.income_controller.update_income(new_data)
        else:
            result = self.outcome_controller.update_outcome(new_data)

        if result.get("valid"):
            self.load_data(transaction["type"])
            PopupSuccess("Success", "berhasil disimpan!")
        else:
            errors = result.get("errors")
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            PopupWarning("Warning", f"Gagal menyimpan!\n{error_message}")

        dialog.accept()

    def confirm_delete(self, transaction):
        """Konfirmasi Delete"""
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
        msg.setWindowTitle("Konfirmasi Hapus")
        msg.setText(f"Apakah Anda yakin ingin menghapus transaksi {transaction['type']} dengan jumlah Rp {transaction['amount']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        result = msg.exec_()
        if result == QMessageBox.Yes:
            if transaction["type"] == "income":
                self.income_controller.delete_income(transaction["id"])
            else:
                self.outcome_controller.delete_outcome(transaction["id"])

            self.load_data(transaction["type"])
            
            info_msg = QMessageBox()
            info_msg.setStyleSheet(msg.styleSheet())
            info_msg.setWindowTitle("Informasi")
            info_msg.setText("Transaksi berhasil dihapus")
            info_msg.exec_()