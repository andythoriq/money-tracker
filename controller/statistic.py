from controller.outcome import Outcome
from controller.income import Income
from controller.wallet import Wallet
import numpy as np
from datetime import datetime, timedelta
from pyqtgraph.Qt import QtWidgets
import calendar

class Statistic:
    def __init__(self):
        super().__init__()
        self.income_controller = Income(Wallet())
        self.outcome_controller = Outcome(Wallet())
        self.cur_data = self.generate_data()

    def generate_data(self, offset = 0, jenis = "harian"):
        # Ambil dan konversi data dari Outcome
        outcome_amount = []
        outcome_date = []
        if self.outcome_controller.load_outcomes() != []:
            for outcome in self.outcome_controller.load_outcomes():

                outcome_amount.append(int(outcome[1]))
                outcome_date.append(outcome[5])
        else:
                outcome_amount.append(0)
                outcome_date.append("01/01/1900")

        # Ambil dan konversi data dari Income
        income_amount = []
        income_date = []
        
        if self.income_controller.load_incomes() != []:
            for income in self.income_controller.load_incomes():
                income_amount.append(int(income[1]))
                income_date.append(income[5])
        else:
                income_amount.append(0)
                income_date.append("01/01/1900")


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

        x = []
        yI = []
        yO = []
        labels = []
        incomeSum = 0
        outcomeSum = 0
        temp = 0

        if (jenis == "harian"):
            for x in self.ubahHari(offset):
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

            for x in self.ubahHari(offset):
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
            time = self.ubahHari(offset) # nama hari
            x = np.arange(len(time))
            description = self.NamaHariDariTanggal(time) # tanggal hari
            labels = [f"{description[i]}\n({time[i]})" for i in range(len(time))]

        if (jenis == "mingguan"):
            BSM = self.BulanSkrngMingguan(offset)
                        
            for x1 in self.BulanSkrngMingguan(offset):
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

            for x1 in self.BulanSkrngMingguan(offset):
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
            time = self.BulanSkrngMingguan(offset) # nama hari
            x = np.arange(len(time))
            for i in range(len(time)):
                time[i] = time[i][0]
            description = ["1st Week", "2nd Week", "3rd Week", "4th Week"] # tanggal hari
            if len(time) == 5:
                description.append("5th Week")
            # Membuat label yang mencakup hari dan tanggal
            labels = [f"{description[i]}\n({time[i]})" for i in range(len(time))]

        if jenis == "bulanan":
            # Konversi sorted_tanggalI menjadi (bulan, tahun)
            tanggal_list = [(int(t.split('/')[1]), int(t.split('/')[2])) for t in sorted_tanggalI]
            # Iterasi melalui bulan dan tahun dari BulanSkrng
            for bulan, tahun in zip(*self.BulanSkrng(offset)):
                temp = 0  # Menyimpan total income per bulan

		        # Iterasi semua tanggal dan mencari yang sesuai
                for i, (b, t) in enumerate(tanggal_list):
                    if (b, t) == (bulan, tahun):  # Jika bulan & tahun cocok
                        temp += sorted_amountI[i]
				
                # Simpan hasil per bulan dan tambahkan ke total
                yI.append(temp)
                incomeSum += temp

            tanggal_list = [(int(t.split('/')[1]), int(t.split('/')[2])) for t in sorted_tanggalO]
            # Iterasi melalui bulan dan tahun dari BulanSkrng
            for bulan, tahun in zip(*self.BulanSkrng(offset)):
                temp = 0  # Menyimpan total income per bulan
        
                # Iterasi semua tanggal dan mencari yang sesuai
                for i, (b, t) in enumerate(tanggal_list):
                    if (b, t) == (bulan, tahun):  # Jika bulan & tahun cocok
                        temp += sorted_amountO[i]
        
                # Simpan hasil per bulan dan tambahkan ke total
                yO.append(temp)
                outcomeSum += temp

            # Data untuk x axis harian
            blnThn = self.BulanSkrng(offset) # nama hari
            time = blnThn[0]
            x = np.arange(len(time))
            description = self.NamaBulanDariAngka(time) # tanggal hari
            labels = [f"{description[i]}\n({blnThn[1][i]})" for i in range(len(time))]
        
        # Data untuk x axis tahunan
        if jenis == "tahunan":
            tanggal_list = [int(t.split('/')[2]) for t in sorted_tanggalI]
			
            for tahun in self.TahunSkrng(offset):
                temp = 0  
            
                for i, t in enumerate(tanggal_list):
                    if t == tahun:  # Jika tahunnya cocok
                        temp += sorted_amountI[i]
						    # Simpan hasil per tahun dan tambahkan ke total
                yI.append(temp)
                incomeSum += temp
			
            tanggal_list = [int(t.split('/')[2]) for t in sorted_tanggalO]
			
            for tahun in self.TahunSkrng(offset):
                temp = 0  
			    
                for i, t in enumerate(tanggal_list):
                    if t == tahun:  # Jika tahunnya cocok
                        temp += sorted_amountO[i]
			
			    # Simpan hasil per tahun dan tambahkan ke total
                yO.append(temp)
                outcomeSum += temp
            time = self.TahunSkrng(offset)
            x = np.arange(len(time))
            labels = [f"{time[i]}" for i in range(len(time))]
        
        return x, yI, yO, labels, incomeSum, outcomeSum

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
        start_of_week = today + timedelta(days=offset * 7)
        return [
            (start_of_week + timedelta(days=i)).strftime("%d/%m/%Y") 
            for i in range(7)
        ]
    
    def BulanSkrngMingguan(self, offset=0):  # Menambahkan parameter offset (default 0)
        today = datetime.today()  # Mendapatkan tanggal hari ini
        
        # Menghitung bulan dan tahun baru berdasarkan offset
        new_month = today.month + offset * 6
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

    def NamaBulanDariAngka(self, angka_bulan):
        # Mengambil nama bulan dalam bahasa Inggris berdasarkan nomor bulan
        return [calendar.month_name[bulan] for bulan in angka_bulan if 1 <= bulan <= 12]

    def BulanSkrng(self, offset=0):
	    # Mendapatkan bulan dan tahun saat ini
        today = datetime.today()
        current_month = today.month
        current_year = today.year
        months = []
        years = []
	
	    # Menentukan bulan awal
        if 6 > current_month >= 12:
            current_month = 12
        elif 1 <= current_month <= 6:
            current_month = 6
        
        # Menyesuaikan dengan offset
        current_month += offset  
	
    
        # Koreksi jika bulan keluar dari rentang 1-12
        while current_month > 12:
            current_month -= 12
            current_year += 1
        while current_month < 1:
            current_month += 12
            current_year -= 1
	
        # Mengisi daftar bulan dan tahun
        for i in range(6):
            months.append(current_month)
            years.append(current_year)
            current_month -= 1
            if current_month == 0:
                current_month = 12
                current_year -= 1
        
        # Membalik urutan agar dari yang lama ke baru
        return months[::-1], years[::-1]

    def TahunSkrng(self, offset=0):
        # Mendapatkan tahun saat ini dan menyesuaikan offset
        today = datetime.today()
        current_year = today.year
        years= []
        
        # Menentukan awal periode 5 tahunan yang benar
        if current_year % 5 == 0:
            start_year = current_year - 4
        else:
            start_year = current_year // 5 * 5 + 1
        
        # Menghasilkan daftar 5 tahun dari start_year
        for i in range(5):
            years.append(start_year + i + offset)
        
        return years

    def generate_statistics(self):
        self.plot_widget.clear()

        data = self.cur_data

        x = data[0]
        income_barItem = data[1]
        outcome_barItem = data[2]
        infoLabels = data[3]
        maxNilai = max(data[1] + data[2])

        # Membuat grafik batang untuk pendapatan (warna hijau) dan pengeluaran (warna merah)
        income_graph = BarGraphItem(x=x-0.15, height=income_barItem, width=0.3, brush='#FF9F40', name="Pendapatan")
        outcome_graph = BarGraphItem(x=x+0.15, height=outcome_barItem, width=0.3, brush='#F4BE37', name="Pengeluaran")

        # Menambahkan grafik batang ke plot
        self.plot_widget.addItem(income_graph)
        self.plot_widget.addItem(outcome_graph)
        # Mengubah ticks sumbu X untuk menampilkan dua informasi: hari dan tanggal
        self.plot_widget.getAxis('bottom').setTicks([list(zip(x, infoLabels))])

        # Mengubah sumbu Y untuk lebih baik menampilkan data
        self.plot_widget.setLabel('left', 'Nilai', units="")
        self.plot_widget.setLabel('bottom', 'Hari dan Tanggal')

        # Display values on top of bars (income bars)
        for i, val in enumerate(income_barItem):
            text = TextItem(str(val), color='green')
            text.setPos(x[i] - 0.25, val + 3)  # Position above the bar
            self.plot_widget.addItem(text)

        # Display values on top of bars (outcome bars)
        for i, val in enumerate(outcome_barItem):
            text = TextItem(str(val), color='red')
            text.setPos(x[i], val + 3)  # Position above the bar
            self.plot_widget.addItem(text)

        # Menyesuaikan format label sumbu Y untuk menghindari notasi ilmiah
        axis = self.plot_widget.getAxis('left')

        # Periksa apakah maxNilai kurang dari 5 dan tentukan langkah minimal
        step = max(1, int(maxNilai / 5))  # Pastikan langkah tidak menjadi 0

        # Membuat ticks dengan langkah yang aman
        ticks = [(i, "{:,.0f}".format(i)) for i in range(0, maxNilai + 1, step)]

        # Menetapkan ticks pada axis
        axis.setTicks([ticks])

        # Tombol untuk mengubah view range setelah beberapa detik
        self.plot_widget.getPlotItem().vb.setRange(yRange=(0, int(maxNilai * 1.3)), padding=0)

        # Menghilangkan toolbar atau elemen lainnya
        self.plot_widget.getPlotItem().hideButtons()  # Menghilangkan tombol atau kontrol lainnya

        # Menambahkan grid pada plot untuk mempermudah pembacaan
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Alpha untuk transparansi grid

        # Menambahkan legenda ke plot
        self.plot_widget.addLegend()  # Ini adalah cara yang benar untuk menambahkan legenda