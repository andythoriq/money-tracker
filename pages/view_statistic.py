import sys  # Import sys untuk mengelola parameter baris perintah dan menjalankan aplikasi
import numpy as np  # Import numpy untuk operasi matematika dan pembuatan data acak
import pandas as pd  # Import pandas untuk manipulasi data (meskipun belum digunakan langsung dalam contoh ini)
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton  # Import widget PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Import FigureCanvas untuk menampilkan grafik di PyQt5
from matplotlib.figure import Figure  # Import Figure untuk membuat grafik dengan Matplotlib

class StatsApp(QMainWindow):
    def __init__(self):
        super().__init__()  # Memanggil konstruktor kelas induk (QMainWindow)
        self.setWindowTitle("Statistik dengan PyQt dan Matplotlib")  # Menetapkan judul window
        
        # Membuat layout utama untuk menampung elemen-elemen GUI
        layout = QVBoxLayout()
        
        # Membuat Figure untuk grafik Matplotlib
        self.figure = Figure()  # Membuat figure kosong untuk grafik
        self.canvas = FigureCanvas(self.figure)  # Membuat canvas yang dapat menampilkan figure
        layout.addWidget(self.canvas)  # Menambahkan canvas ke layout
        
        # Membuat tombol yang ketika diklik akan menghasilkan data statistik
        self.button = QPushButton("Generate Statistik")  # Membuat tombol
        self.button.clicked.connect(self.generate_statistics)  # Menghubungkan tombol dengan metode untuk menghasilkan statistik
        layout.addWidget(self.button)  # Menambahkan tombol ke layout
        
        # Membuat widget utama untuk menampung layout
        container = QWidget()  # Membuat container widget
        container.setLayout(layout)  # Menetapkan layout pada container
        self.setCentralWidget(container)  # Menetapkan container sebagai widget utama dari window
        
    def generate_statistics(self):
        # Contoh data acak: menghasilkan 1000 data yang terdistribusi normal
        data = np.random.normal(0, 1, 1000)  # Distribusi normal dengan mean 0 dan std dev 1
        
        # Menghitung statistik dasar
        mean = np.mean(data)  # Rata-rata dari data
        median = np.median(data)  # Median dari data
        std_dev = np.std(data)  # Deviasi standar dari data
        
        # Mencetak statistik ke konsol
        print(f"Mean: {mean}")
        print(f"Median: {median}")
        print(f"Standard Deviation: {std_dev}")
        
        # Membersihkan figure (hapus grafik sebelumnya)
        self.figure.clf()  # Menghapus figure sebelumnya agar tidak ada tumpang tindih

        # Membuat plot histogram menggunakan Matplotlib
        ax = self.figure.add_subplot(111)  # Menambahkan subplot (grafik) ke figure
        ax.hist(data, bins=30, color='blue', alpha=0.7)  # Membuat histogram dari data dengan 30 bin
        ax.set_title("Histogram Data Normal")  # Menambahkan judul ke grafik
        ax.set_xlabel("Nilai")  # Menambahkan label untuk sumbu X
        ax.set_ylabel("Frekuensi")  # Menambahkan label untuk sumbu Y
        
        # Menyegarkan canvas untuk menampilkan grafik terbaru
        self.canvas.draw()

# Mengeksekusi aplikasi PyQt jika file ini dijalankan secara langsung
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Membuat instance QApplication yang mengelola event loop
    window = StatsApp()  # Membuat window aplikasi
    window.show()  # Menampilkan window aplikasi
    sys.exit(app.exec_())  # Memulai event loop dan keluar ketika aplikasi selesai

'''
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StatsApp(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def generate_statistics(self):
        # Contoh data pengeluaran harian (misalnya selama 30 hari)
        days = np.arange(1, 31)  # 30 hari
        expenditures = np.random.randint(100, 500, 30)  # Pengeluaran acak dalam rentang 100 - 500

        self.figure.clf()

        ax = self.figure.add_subplot(111)
        ax.plot(days, expenditures, label="Pengeluaran Harian", color='blue')
        ax.set_title("Grafik Pengeluaran Harian")
        ax.set_xlabel("Hari")
        ax.set_ylabel("Pengeluaran (Rupiah)")
        ax.legend()

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatsApp()
    window.show()
    sys.exit(app.exec_())

'''