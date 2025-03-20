from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QLabel, QRadioButton, 
    QButtonGroup, QDialog, QFormLayout, QSpinBox, 
    QComboBox, QLineEdit, QCalendarWidget, QMessageBox
)
from datetime import datetime
from controller.income import Income
from controller.outcome import Outcome
from controller.wallet import Wallet
from controller.category import Category

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.category_controller = Category()
        self.income_controller = Income(self.wallet_controller)
        self.outcome_controller = Outcome(self.wallet_controller)
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        layout = QVBoxLayout()

        # Radio Button Filter
        btn_layout = QHBoxLayout()
        self.radio_group = QButtonGroup(self)

        self.radio_income = QRadioButton("Income")
        self.radio_outcome = QRadioButton("Outcome")
        self.radio_all = QRadioButton("Semua")

        self.radio_group.addButton(self.radio_income)
        self.radio_group.addButton(self.radio_outcome)
        self.radio_group.addButton(self.radio_all)

        self.radio_all.setChecked(True)
        self.radio_income.toggled.connect(lambda: self.load_data("income"))
        self.radio_outcome.toggled.connect(lambda: self.load_data("outcome"))
        self.radio_all.toggled.connect(lambda: self.load_data("all"))

        btn_layout.addWidget(self.radio_income)
        btn_layout.addWidget(self.radio_outcome)
        btn_layout.addWidget(self.radio_all)
        layout.addLayout(btn_layout)

        # Tabel Transaksi
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Jumlah", "Kategori", "Dompet", "Deskripsi", "Edit", "Delete"])
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        # Label Total
        self.label = QLabel(f"Total : Rp 0")
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.load_data("all")

    def load_data(self, filter_type):
        """Memuat data ke tabel berdasarkan filter"""
        self.table.setRowCount(0)
        transactions = []
        total = 0

        # Load data income
        for income in self.income_controller.load_incomes():
            transactions.append({
                "id": income[0],
                "date": datetime.strptime(income[5], "%d/%m/%Y"),
                "type": "income",
                "amount": income[1],
                "category": income[2],
                "wallet": income[3],
                "desc": income[4]
            })

        # Load data outcome
        for outcome in self.outcome_controller.load_outcomes():
            transactions.append({
                "id": outcome[0],
                "date": datetime.strptime(outcome[5], "%d/%m/%Y"),
                "type": "outcome",
                "amount": outcome[1],
                "category": outcome[2],
                "wallet": outcome[3],
                "desc": outcome[4]
            })

        # Filter transaksi
        if filter_type == "income":
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
            btn_edit.clicked.connect(lambda _, t=transaction: self.open_edit_popup(t))
            self.table.setCellWidget(row, 6, btn_edit)

            # Tombol Delete
            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(lambda _, t=transaction: self.confirm_delete(t))
            self.table.setCellWidget(row, 7, btn_delete)

        self.label.setText(f"Total : Rp {total}")

    def open_edit_popup(self, transaction):
        """Popup Edit Data"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Transaksi")
        layout = QFormLayout(dialog)

        # Widget Form
        amount_input = QSpinBox()
        amount_input.setMaximum(100000000)
        amount_input.setValue(int(transaction["amount"]))

        category_input = QComboBox()
        category_input.addItems(self.category_controller.load_category_names(transaction["type"]))
        category_input.setCurrentText(transaction["category"])

        wallet_input = QComboBox()
        wallet_input.addItems(self.wallet_controller.load_wallet_names())
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
        btn_save.clicked.connect(lambda: self.save_edit(transaction, amount_input, category_input, wallet_input, desc_input, date_input, dialog))
        layout.addRow(btn_save)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edit(self, transaction, amount, category, wallet, desc, date, dialog):
        """Simpan perubahan edit transaksi"""
        new_data = [transaction["id"], str(amount.value()), category.currentText(), wallet.currentText(), desc.text(), date.selectedDate().toString("dd/MM/yyyy")]

        if transaction["type"] == "income":
            self.income_controller.update_income(new_data)
        else:
            self.outcome_controller.update_outcome(new_data)

        dialog.accept()
        self.load_data(transaction["type"])

    def confirm_delete(self, transaction):
        """Konfirmasi Delete"""
        msg = QMessageBox.question(self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus transaksi {transaction['type']} dengan jumlah Rp {transaction['amount']}?",
            QMessageBox.Yes | QMessageBox.No)

        if msg == QMessageBox.Yes:
            if transaction["type"] == "income":
                self.income_controller.delete_income(transaction["id"])
            else:
                self.outcome_controller.delete_outcome(transaction["id"])

            self.load_data(transaction["type"])
            QMessageBox.information(self, "Informasi", "Transaksi berhasil dihapus")
