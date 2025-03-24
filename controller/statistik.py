from income import Income
from outcome import Outcome
from wallet import Wallet
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from datetime import datetime, timedelta
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

class StatsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.income_controller = Income(Wallet())
        self.outcome_controller = Outcome(Wallet())
        self.offset = 0
        self.jenis = 0
        self.cur_data = self.generate_data(self.offset)
        self.init_ui()

    def init_ui(self):
        """Inisialisasi UI"""
        self.setWindowTitle("Statistik Pengeluaran Harian")
        # Membuat layout untuk menampung plot dan widget lainnya
        layout = QtWidgets.QVBoxLayout()

        # Membuat plot
        self.plot_widget = pg.PlotWidget()
        # Mengubah latar belakang plot menjadi putih
        self.plot_widget.setBackground('w')
        # Menonaktifkan kemampuan untuk menggeser dan zoom plot
        self.plot_widget.setMouseEnabled(x=False, y=False)
        # Menambahkan plot ke layout
        layout.addWidget(self.plot_widget)

        # Membuat tombol untuk menghasilkan plot
        generate_button = QtWidgets.QPushButton('Generate Plot')
        generate_button.clicked.connect(self.generate_statistics)
        layout.addWidget(generate_button)

        # Membuat tombol untuk menghasilkan plot
        next_button = QtWidgets.QPushButton('Next Plot')
        next_button.clicked.connect(lambda: self.change_offset('next'))
        layout.addWidget(next_button)

        # Membuat tombol untuk menghasilkan plot 
        prev_button = QtWidgets.QPushButton('Prev Plot')
        prev_button.clicked.connect(lambda: self.change_offset('prev'))
        layout.addWidget(prev_button)

        # Membuat tombol untuk menyimpan plot
        save_button = QtWidgets.QPushButton("Save Graph")
        save_button.clicked.connect(self.save_graph)
        layout.addWidget(save_button)

        # Membuat tombol untuk menghapus plot
        delete_button = QtWidgets.QPushButton('Delete Plot')
        delete_button.clicked.connect(self.delete_plot)
        layout.addWidget(delete_button)

        # Membuat ComboBox di kanan atas
        combo_box = QtWidgets.QComboBox()
        combo_box.addItem('Option 1')
        combo_box.addItem('Option 2')
        combo_box.addItem('Option 3')
        layout.addWidget(combo_box)

        # Membuat container untuk layout
        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)

        # Load data awal (semua transaksi)
        self.generate_statistics()

    def generate_data(self, offset = 0, jenis = "harian"):
        # Ambil dan konversi data dari Outcome
        outcome_amount = []
        outcome_date = []
        for outcome in self.outcome_controller.load_outcomes():

            outcome_amount.append(int(outcome[1]))
            outcome_date.append(outcome[5])

        # Ambil dan konversi data dari Income
        income_amount = []
        income_date = []
        for income in self.income_controller.load_incomes():
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
    

        yI = []
        yO = []
        incomeSum = 0
        outcomeSum = 0
        temp = 0

        if (jenis == "harian"):
            for x in self.ubahHari(self.offset):
                try:
                    indeks = sorted_tanggalI.index(x)
                    temp += sorted_amountI[indeks]
                    while True:
                        if indeks + 1 < len(sorted_tanggalI) and sorted_tanggalI[indeks + 1] == x:
                            indeks += 1
                            if sorted_tanggalI[indeks] == x:
                                temp += sorted_amountI[indeks]
                        else:
                            yI.append(temp)
                            incomeSum += temp
                            temp = 0
                            break
                except ValueError:
                    yI.append(0)

            for x in self.ubahHari(self.offset):
                try:
                    indeks = sorted_tanggalO.index(x)
                    temp += sorted_amountO[indeks]
                    while True:
                        if indeks + 1 < len(sorted_tanggalO) and sorted_tanggalO[indeks + 1] == x:
                            indeks += 1
                            if sorted_tanggalO[indeks] == x:
                                temp += sorted_amountO[indeks]
                        else:
                            yO.append(temp)
                            outcomeSum += temp
                            temp = 0
                            break
                except ValueError:
                    yO.append(0)

            # Data untuk x axis harian
            time = self.ubahHari(self.offset) # nama hari
            description = self.NamaHariDariTanggal(time) # tanggal hari
            labels = [f"{description[i]}\n({time[i]})" for i in range(len(time))]

        if (jenis == "mingguan"):
            BSM = self.BulanSkrngMingguan(self.offset)
            for itemsList in range(len(BSM)):
                for item in range(len(BSM[itemsList])):
                    if BSM[itemsList][item][0] == '0':
                        BSM[itemsList][item] = BSM[itemsList][item][1:]
                    if BSM[itemsList][item][2] == '0':
                        BSM[itemsList][item] = BSM[itemsList][item][0:2] + BSM[itemsList][item][3:]
                    if BSM[itemsList][item][3] == '0':
                        BSM[itemsList][item] = BSM[itemsList][item][0:3] + BSM[itemsList][item][4:]
                        
            for x1 in BSM:
                for x2 in x1:
                    try:
                        indeks = sorted_tanggalI.index(x2)
                        temp += sorted_amountI[indeks]
                        while True:
                            if indeks + 1 < len(sorted_tanggalI) and sorted_tanggalI[indeks + 1] == x2:
                                indeks += 1
                                if sorted_tanggalI[indeks] == x2:
                                    temp += sorted_amountI[indeks]
                            else:
                                incomeSum += temp
                                break
                        if not (indeks + 1 < len(sorted_tanggalI) and sorted_tanggalI[indeks + 1] == x2):
                            continue                    
                    except ValueError:
                        continue
                yI.append(temp)
                temp = 0

            for x1 in BSM:
                for x2 in x1:
                    try:
                        indeks = sorted_tanggalO.index(x2)
                        temp += sorted_amountO[indeks]
                        while True:
                            if indeks + 1 < len(sorted_tanggalO) and sorted_tanggalO[indeks + 1] == x2:
                                indeks += 1
                                if sorted_tanggalO[indeks] == x2:
                                    temp += sorted_amountO[indeks]
                            else:
                                outcomeSum += temp
                                break
                        if not(indeks + 1 < len(sorted_tanggalO) and sorted_tanggalO[indeks + 1] == x2):
                            continue
                    except ValueError:
                        continue
                yO.append(temp)
                temp = 0
            
            # Data untuk x axis harian
            time = BSM # nama hari
            for x in range(len(time)):
                time[x] = time[x][0]
            description = ["1st Week", "2nd Week", "3rd Week", "4th Week"] # tanggal hari
            if len(time) == 5:
                description.append("5th Week")
            # Membuat label yang mencakup hari dan tanggal
            labels = [f"{description[i]}\n({time[i]})" for i in range(len(time))]

        if (jenis == "bulanan"):
            for x in self.ubahHari(self.offset):
                try:
                    indeks = sorted_tanggalI.index(x)
                    temp += sorted_amountI[indeks]
                    while True:
                        if indeks + 1 < len(sorted_tanggalI) and sorted_tanggalI[indeks + 1] == x:
                            indeks += 1
                            if sorted_tanggalI[indeks] == x:
                                temp += sorted_amountI[indeks]
                        else:
                            yI.append(temp)
                            incomeSum += temp
                            temp = 0
                            break
                except ValueError:
                    yI.append(0)

            for x in self.ubahHari(self.offset):
                try:
                    indeks = sorted_tanggalO.index(x)
                    temp += sorted_amountO[indeks]
                    while True:
                        if indeks + 1 < len(sorted_tanggalO) and sorted_tanggalO[indeks + 1] == x:
                            indeks += 1
                            if sorted_tanggalO[indeks] == x:
                                temp += sorted_amountO[indeks]
                        else:
                            yO.append(temp)
                            outcomeSum += temp
                            temp = 0
                            break
                except ValueError:
                    yO.append(0)

            # Data untuk x axis harian
            time = self.ubahHari(self.offset) # nama hari
            description = self.NamaHariDariTanggal(time) # tanggal hari
            labels = [f"{description[i]}\n({time[i]})" for i in range(len(time))]
        
        # Data untuk x axis tahunan
        # time = self.TahunSkrng() # urutan tahunan

        income_barItem = yI  # Data untuk sumbu y
        outcome_barItem = yO  # Data untuk sumbu y2

        # Menggunakan np.arange untuk membuat sumbu x
        x = np.arange(len(time))  # Akan menghasilkan 7 hari
        
        return x, yI, yO, labels

    def generate_statistics(self):
        self.plot_widget.clear()

        data = self.cur_data

        x = data[0]
        income_barItem = data[1]
        outcome_barItem = data[2]
        infoLabels = data[3]

        # Membuat grafik batang untuk pendapatan (warna hijau) dan pengeluaran (warna merah)
        income_graph = pg.BarGraphItem(x=x-0.15, height=income_barItem, width=0.3, brush='g', name="Pendapatan")
        outcome_graph = pg.BarGraphItem(x=x+0.15, height=outcome_barItem, width=0.3, brush='r', name="Pengeluaran")

        # Menambahkan grafik batang ke plot
        self.plot_widget.addItem(income_graph)
        self.plot_widget.addItem(outcome_graph)

        # Mengubah ticks sumbu X untuk menampilkan dua informasi: hari dan tanggal
        self.plot_widget.getAxis('bottom').setTicks([list(zip(x, infoLabels))])

        # Mengubah sumbu Y untuk lebih baik menampilkan data
        self.plot_widget.setLabel('left', 'Nilai')
        self.plot_widget.setLabel('bottom', 'Hari dan Tanggal')

        # Menambahkan grid pada plot untuk mempermudah pembacaan
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Alpha untuk transparansi grid

        # Menambahkan legenda ke plot
        self.plot_widget.addLegend()  # Ini adalah cara yang benar untuk menambahkan legenda

    # Fungsi untuk menyimpan grafik
    def save_graph(self):
        # Mendapatkan path file untuk menyimpan gambar
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Graph", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            # Mengambil snapshot dari widget plot
            pixmap = self.plot_widget.grab()  # Mengambil screenshot dari plot_widget

            # Menyimpan snapshot sebagai file
            pixmap.save(file_path)  # Menyimpan gambar

    # Fungsi untuk menghapus plot
    def delete_plot(self):
        self.plot_widget.clear()
        # Menghapus label dan ticks pada sumbu X dan Y
        self.plot_widget.getAxis('bottom').setTicks([])  # Hapus ticks pada sumbu X
        # plot_widget.getAxis('left').setTicks([])    # Hapus ticks pada sumbu Y
        self.plot_widget.setLabel('left', '')            # Menghapus label sumbu Y
        self.plot_widget.setLabel('bottom', '')          # Menghapus label sumbu X

    def NamaHariDariTanggal(self, tanggal_list):
        # Mengonversi tanggal dalam format "day/month/year" menjadi objek datetime dan mengambil nama hari
        return [datetime.strptime(tanggal, "%d/%m/%Y").strftime("%A") for tanggal in tanggal_list]

    def NamaBulanDariTanggal(self, tanggal_list):
        return [datetime.strptime(tanggal, "%d/%m/%Y").strftime("%B") for tanggal in tanggal_list]
    
    def ubahHari(self, offset=0):
        today = datetime.today()
        start_of_week = today + timedelta(days=offset)
        return [f"{(start_of_week + timedelta(days=i)).day}/{(start_of_week + timedelta(days=i)).month}/{(start_of_week + timedelta(days=i)).year}" for i in range(7)]

    def MingguSkrng(self, offset=0):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday(), weeks=-offset)  # Start of the week, adjusted by the offset
        return [f"{(start_of_week + timedelta(days=i)).day}/{(start_of_week + timedelta(days=i)).month}/{(start_of_week + timedelta(days=i)).year}" for i in range(7)]

    def BulanSkrngMingguan(self, offset=0):  # Menambahkan parameter offset (default 0)
        today = datetime.today()  # Mendapatkan tanggal hari ini
        
        # Menghitung bulan dan tahun baru berdasarkan offset
        new_month = today.month + offset
        new_year = today.year
        
        # Jika bulan baru melebihi Desember, sesuaikan tahun
        if new_month > 12:
            new_month -= 12
            new_year += 1
        elif new_month < 1:
            new_month += 12
            new_year -= 1
        
        # Menghitung hari pertama dari bulan baru
        first_day = datetime(new_year, new_month, 1)
        
        next_month = datetime(new_year, new_month + 1, 1) if new_month < 12 else datetime(new_year + 1, 1, 1)
        last_day = next_month - timedelta(days=1)  # Hari terakhir bulan tersebut
        
        minggu = []  # List untuk menyimpan minggu
        current_week_start = first_day
        
        # Loop untuk membagi bulan menjadi minggu
        while current_week_start <= last_day:
            current_week_end = min(current_week_start + timedelta(days=6), last_day)
            minggu.append([ (current_week_start + timedelta(days=i)).strftime("%d/%m/%Y") 
                           for i in range((current_week_end - current_week_start).days + 1)])
            current_week_start = current_week_end + timedelta(days=1)

        return minggu

    from datetime import datetime

    def BulanSkrng(self, offset=0):
        # Mendapatkan bulan dan tahun saat ini
        today = datetime.today()
        current_month = today.month + offset  # Menghitung bulan baru dengan offset
                
        # Mengembalikan list bulan yang sesuai dengan bulan saat ini
        if current_month <= 6:
            return [1, 2, 3, 4, 5, 6], today.year
        else:
            return [7, 8, 9, 10, 11, 12], today.year

    def change_offset(self, direction):
        if direction == 'next':
            self.offset += 1
        elif direction == 'prev':
            self.offset -= 1
        self.cur_data = self.generate_data(self.offset)
        self.generate_statistics()

    def go_back(self):
        """Kembali ke Dashboard"""
        if self.parent():
            self.parent().setCurrentIndex(0)  # Indeks 0 adalah dashboard

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatsApp()
    window.show()
    sys.exit(app.exec_())