import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from income import Income
from outcome import Outcome
from wallet import Wallet
from datetime import datetime

class StatsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.income_controller = Income(Wallet())
        self.outcome_controller = Outcome(Wallet())
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle("Statistik Pengeluaran Harian")
        layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.button = QPushButton("Generate Statistik Pengeluaran")
        self.button.clicked.connect(self.generate_statistics)
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # Tombol kembali ke dashboard
        self.btn_back = QPushButton("Kembali ke Dashboard")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        # Load data awal (semua transaksi)
        self.generate_statistics()

    def generate_statistics(self, rentang="bulanan", waktu=datetime.now().date()):
        # Get the current date
        current_date = datetime.now().date()
        # Mendapatkan minggu dari tanggal saat ini
        current_week = pd.to_datetime(current_date).isocalendar().week

        # Contoh data pengeluaran mingguan (misalnya selama 7 hari)
        days = np.arange(0, 7)  # 7 hari

        # Ambil dan konversi data dari Income
        data_amount = []
        data_date = []
        for income in self.income_controller.load_incomes():
            data_amount.append(income[1])
            data_date.append(income[5])

        expenditures = np.random.randint(100, 500, 7)  # Pengeluaran acak dalam rentang 100 - 500

        self.figure.clf()  # Membersihkan figure sebelum menggambar ulang

        # Membuat subplot dan mengganti plot menjadi diagram batang
        ax = self.figure.add_subplot(111)
        ax.bar(data_date, data_amount, color='blue')  # Mengganti plot dengan bar chart
        ax.set_title("Diagram Batang Pengeluaran Harian")
        ax.set_xlabel("Hari")
        ax.set_ylabel("Pengeluaran (Rupiah)")

        self.canvas.draw()  # Menggambar ulang canvas dengan perubahan

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah dashboard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatsApp()
    window.show()
    sys.exit(app.exec_())