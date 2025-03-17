"""
Simple example using BarGraphItem
"""
from income import Income
from outcome import Outcome
from wallet import Wallet
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from datetime import datetime, timedelta

def NamaHariDariTanggal(tanggal_list):
    # Mengonversi tanggal dalam string menjadi objek datetime dan mengambil nama hari
    return [datetime.strptime(tanggal, "%Y-%m-%d").strftime("%A") for tanggal in tanggal_list]

def MingguSkrng(offset=0):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday(), weeks=-offset)  # Geser minggu
    return [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def BulanSkrngMingguan():
    today = datetime.today()
    first_day = datetime(today.year, today.month, 1)  # Hari pertama bulan ini
    next_month = datetime(today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)
    last_day = next_month - timedelta(days=1)  # Hari terakhir bulan ini
    
    minggu = []
    current_week_start = first_day
    
    # Loop untuk membagi tanggal menjadi minggu
    while current_week_start <= last_day:
        current_week_end = min(current_week_start + timedelta(days=6), last_day)
        minggu.append([ (current_week_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((current_week_end - current_week_start).days + 1)])
        current_week_start = current_week_end + timedelta(days=1)

    return minggu

# Contoh pemanggilan fungsi
for minggu in BulanSkrngMingguan():
    print(minggu)

# Ambil dan konversi data dari Outcome
outcome_amount = []
outcome_date = []
for outcome in Outcome(Wallet()).load_outcomes():
    outcome_amount.append(int(outcome[1]))
    outcome_date.append(outcome[5])

# Ambil dan konversi data dari Income
income_amount = []
income_date = []
for income in Income(Wallet()).load_incomes():
    income_amount.append(int(income[1]))
    income_date.append(income[5])

# Menggabungkan kedua list dan menyortir berdasarkan tanggal
sorted_listI = sorted(zip(income_date, income_amount), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
sorted_listO = sorted(zip(outcome_date, outcome_amount), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))

# Memisahkan kembali menjadi dua list
sorted_tanggalI, sorted_amountI = zip(*sorted_listI)
sorted_tanggalO, sorted_amountO = zip(*sorted_listO)

# Mengonversi ke list
sorted_tanggalI = list(sorted_tanggalI)
sorted_amountI = list(sorted_amountI)
sorted_tanggalO = list(sorted_tanggalO)
sorted_amountO = list(sorted_amountO)

# Membuat aplikasi Qt
app = QtWidgets.QApplication([])

# Membuat jendela utama
window = QtWidgets.QWidget()
window.setWindowTitle('Grafik dengan ComboBox')

# Membuat layout untuk menampung plot dan widget lainnya
layout = QtWidgets.QVBoxLayout()

# Membuat plot
plot_widget = pg.PlotWidget()

# Mengubah latar belakang plot menjadi putih
plot_widget.setBackground('w')

# Menonaktifkan kemampuan untuk menggeser dan zoom plot
plot_widget.setMouseEnabled(x=False, y=False)

# Menambahkan plot ke layout
layout.addWidget(plot_widget)

# Data untuk x dan y
tanggal = BulanSkrngMingguan()[0]# nama hari
hari = NamaHariDariTanggal(tanggal) # tanggal hari

y = np.random.randint(100, 500, len(hari))  # Data untuk sumbu y
y2 = np.random.randint(100, 500, len(hari))  # Data untuk sumbu y2

# Menggunakan np.arange untuk membuat sumbu x
x = np.arange(len(hari))  # Akan menghasilkan 7 hari

# Membuat grafik batang
bar_graph = pg.BarGraphItem(x=x-0.15, height=y, width=0.3, brush='b')
bar_graph2 = pg.BarGraphItem(x=x+0.15, height=y2, width=0.3, brush='g')

# Menambahkan grafik batang ke plot
plot_widget.addItem(bar_graph)
plot_widget.addItem(bar_graph2)

# Membuat label yang mencakup hari dan tanggal
labels = [f"{hari[i]}\n({tanggal[i]})" for i in range(len(hari))]

# Mengubah ticks sumbu X untuk menampilkan dua informasi: hari dan tanggal
plot_widget.getAxis('bottom').setTicks([list(zip(x, labels))])

# Mengubah sumbu Y untuk lebih baik menampilkan data
plot_widget.setLabel('left', 'Nilai')
plot_widget.setLabel('bottom', 'Hari dan Tanggal')

# Menambahkan tombol untuk menyimpan grafik
def save_graph():
    # Menggunakan export() untuk menyimpan grafik sebagai gambar
    file_path, _ = QtWidgets.QFileDialog.getSaveFileName(window, "Save Graph", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
    if file_path:
        plot_widget.export(file_path)  # Menyimpan grafik ke file

save_button = QtWidgets.QPushButton("Save Graph")
save_button.clicked.connect(save_graph)
layout.addWidget(save_button)

# Membuat ComboBox di kanan atas
# combo_box = QtWidgets.QComboBox()
# combo_box.addItem('Option 1')
# combo_box.addItem('Option 2')
# combo_box.addItem('Option 3')

# Menambahkan ComboBox ke layout
# layout.addWidget(combo_box)

# Menambahkan layout ke jendela utama
window.setLayout(layout)

# Menampilkan jendela utama
window.show()

# Menjalankan aplikasi Qt
app.exec_()