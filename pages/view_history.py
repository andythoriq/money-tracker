from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
from datetime import datetime
from controller.income import Income
from controller.outcome import Outcome
from controller.wallet import Wallet

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.income_controller = Income(Wallet())
        self.outcome_controller = Outcome(Wallet())
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        layout = QVBoxLayout()

        # Tombol kembali ke dashboard
        self.btn_back = QPushButton("Kembali ke Dashboard")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        # Tombol Filter (Income, Outcome, Semua)
        btn_layout = QHBoxLayout()
        self.btn_income = QPushButton("Income")
        self.btn_income.clicked.connect(lambda: self.load_data("income"))

        self.btn_outcome = QPushButton("Outcome")
        self.btn_outcome.clicked.connect(lambda: self.load_data("outcome"))

        self.btn_all = QPushButton("Semua")
        self.btn_all.clicked.connect(lambda: self.load_data("all"))

        btn_layout.addWidget(self.btn_income)
        btn_layout.addWidget(self.btn_outcome)
        btn_layout.addWidget(self.btn_all)

        layout.addLayout(btn_layout)

        # Tabel Transaksi
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Jumlah", "Kategori", "Dompet"])
        self.table.setSortingEnabled(True)  # Mengaktifkan sorting

        layout.addWidget(self.table)

        # Text Total
        self.label = QLabel(f"Total : ")
        layout.addWidget(self.label)

        self.setLayout(layout)

        # Load data awal (semua transaksi)
        self.load_data("all")

    def load_data(self, filter_type):
        """Memuat data ke tabel berdasarkan filter"""
        self.table.setRowCount(0)  # Hapus isi tabel
        transactions = []
        total = 0

        # Ambil dan konversi data dari Income
        for income in self.income_controller.load_incomes():
            try:
                parsed_date = datetime.strptime(income[5], "%d/%m/%Y")
            except ValueError:
                print(f"Warning: Format tanggal salah -> {income[5]}")
                parsed_date = datetime.today()  # Default ke hari ini jika error

            transactions.append({
                "date": parsed_date,
                "type": "Income",
                "amount": income[1],
                "category": income[2],
                "wallet": income[3]
            })

        # Ambil dan konversi data dari Outcome
        for outcome in self.outcome_controller.load_outcomes():
            try:
                parsed_date = datetime.strptime(outcome[5], "%d/%m/%Y")
            except ValueError:
                print(f"Warning: Format tanggal salah -> {outcome[5]}")
                parsed_date = datetime.today()  # Default ke hari ini jika error

            transactions.append({
                "date": datetime.strptime(outcome[5], "%d/%m/%Y"),  # Ubah string tanggal ke datetime
                "type": "Outcome",
                "amount": outcome[1],
                "category": outcome[2],
                "wallet": outcome[3]
            })

        # Filter transaksi
        if filter_type == "income":
            transactions = [t for t in transactions if t["type"] == "Income"]
        elif filter_type == "outcome":
            transactions = [t for t in transactions if t["type"] == "Outcome"]

        # Urutkan berdasarkan tanggal
        transactions.sort(key=lambda x: x["date"], reverse=True)

        # Tampilkan data di tabel
        self.table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            if transaction["type"] == "Income":
                total += int(transaction["amount"])
            elif transaction["type"] == "Outcome":
                total -= int(transaction["amount"])

            if isinstance(transaction["date"], datetime):
                date_str = transaction["date"].strftime("%d/%m/%Y")
            else:
                date_str = transaction["date"]  # Jika sudah string, biarkan
            self.table.setItem(row, 0, QTableWidgetItem(date_str))

            self.table.setItem(row, 1, QTableWidgetItem(transaction["type"]))
            amnt = transaction["amount"]
            self.table.setItem(row, 2, QTableWidgetItem(f"Rp - {amnt}"))
            self.table.setItem(row, 3, QTableWidgetItem(transaction["category"]))
            self.table.setItem(row, 4, QTableWidgetItem(transaction["wallet"]))

        # Tampilkan Total
        self.label.setText(f"Total : Rp {total}")

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah dashboard
