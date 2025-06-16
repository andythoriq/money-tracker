from controller.outcome import Outcome
from controller.income import Income
from controller.wallet import Wallet
import numpy as np
from pyqtgraph import TextItem, BarGraphItem
from datetime import datetime, timedelta
from pyqtgraph.Qt import QtWidgets
import calendar
# from controller.setting import Translation

class Statistic:
    def __init__(self):
        super().__init__()
        self.income_controller = Income(Wallet())
        self.outcome_controller = Outcome(Wallet())
        self.offset = 0
        self.jenis = "harian"
        self.cur_data = self.generate_data()
        self.cur_balance = sum(int(income.get("amount")) for income in self.income_controller.load_incomes()) - sum(int(outcome.get("amount")) for outcome in self.outcome_controller.load_outcomes())
        self.net = self.cur_data[4][0] - self.cur_data[4][1]
        self.new_balance = self.cur_balance - self.net

    def generate_data(self):
        # Load and sort income
        income_data = self.income_controller.load_incomes() or [{"amount": 0, "date": "01/01/1900"}]
        sorted_income = sorted(
            [(d["date"], int(d["amount"])) for d in income_data],
            key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")
        )
        income_dates, income_amounts = zip(*sorted_income)

        # Load and sort outcome
        outcome_data = self.outcome_controller.load_outcomes() or [{"amount": 0, "date": "01/01/1900"}]
        sorted_outcome = sorted(
            [(d["date"], int(d["amount"])) for d in outcome_data],
            key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")
        )
        outcome_dates, outcome_amounts = zip(*sorted_outcome)

        # Convert to list
        income_dates, income_amounts = list(income_dates), list(income_amounts)
        outcome_dates, outcome_amounts = list(outcome_dates), list(outcome_amounts)

        yI, yO, labels = [], [], []
        incomeSum, outcomeSum = 0, 0

        if self.jenis == "harian":
            hari_list = self.ubahHari(self.offset)
            for h in hari_list:
                income_total = sum(a for d, a in zip(income_dates, income_amounts) if d == h)
                outcome_total = sum(a for d, a in zip(outcome_dates, outcome_amounts) if d == h)
                yI.append(income_total)
                yO.append(outcome_total)
                incomeSum += income_total
                outcomeSum += outcome_total
            deskripsi = self.NamaHariDariTanggal(hari_list)
            labels = [f"{deskripsi[i]}\n({hari_list[i]})" for i in range(len(hari_list))]
            x = np.arange(len(hari_list))

        elif self.jenis == "mingguan":
            minggu_list = self.BulanSkrngMingguan(self.offset)
            for minggu in minggu_list:
                income_total = sum(
                    a for d, a in zip(income_dates, income_amounts) if d in minggu
                )
                outcome_total = sum(
                    a for d, a in zip(outcome_dates, outcome_amounts) if d in minggu
                )
                yI.append(income_total)
                yO.append(outcome_total)
                incomeSum += income_total
                outcomeSum += outcome_total
            minggu_labels = ["1st Week", "2nd Week", "3rd Week", "4th Week", "5th Week"][:len(minggu_list)]
            time = [m[0] for m in minggu_list]
            labels = [f"{minggu_labels[i]}\n({time[i]})" for i in range(len(time))]
            x = np.arange(len(time))

        elif self.jenis == "bulanan":
            bulan_list = self.BulanSkrng(self.offset)
            tanggal_income = [(int(d.split('/')[1]), int(d.split('/')[2])) for d in income_dates]
            tanggal_outcome = [(int(d.split('/')[1]), int(d.split('/')[2])) for d in outcome_dates]

            for bulan, tahun in zip(*bulan_list):
                income_total = sum(a for (b, t), a in zip(tanggal_income, income_amounts) if (b, t) == (bulan, tahun))
                outcome_total = sum(a for (b, t), a in zip(tanggal_outcome, outcome_amounts) if (b, t) == (bulan, tahun))
                yI.append(income_total)
                yO.append(outcome_total)
                incomeSum += income_total
                outcomeSum += outcome_total
            bulan_nama = self.NamaBulanDariAngka(bulan_list[0])
            labels = [f"{bulan_nama[i]}\n({bulan_list[1][i]})" for i in range(len(bulan_list[0]))]
            x = np.arange(len(bulan_list[0]))

        elif self.jenis == "tahunan":
            tahun_list = self.TahunSkrng(self.offset)
            tahun_income = [int(d.split('/')[2]) for d in income_dates]
            tahun_outcome = [int(d.split('/')[2]) for d in outcome_dates]

            for tahun in tahun_list:
                income_total = sum(a for t, a in zip(tahun_income, income_amounts) if t == tahun)
                outcome_total = sum(a for t, a in zip(tahun_outcome, outcome_amounts) if t == tahun)
                yI.append(income_total)
                yO.append(outcome_total)
                incomeSum += income_total
                outcomeSum += outcome_total
            labels = [str(t) for t in tahun_list]
            x = np.arange(len(tahun_list))

        return x, yI, yO, labels, [incomeSum, outcomeSum]

    def update_data(self, direction):
        if direction == 'next':
            self.offset += 1
        elif direction == 'prev':
            self.offset -= 1

        # Generate data baru berdasarkan offset yang baru
        self.cur_data = self.generate_data()

        # Update net & balance
        self.net = self.cur_data[4][0] - self.cur_data[4][1]
        self.new_balance = self.cur_balance - self.net

    # Fungsi untuk menyimpan grafik
    def save_graph(self, parent_widget, plot_widget):
        # Mendapatkan path file untuk menyimpan gambar
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(parent_widget, "Save Graph", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            # Mengambil snapshot dari widget plot
            pixmap = plot_widget.grab()  # Mengambil screenshot dari plot_widget

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
    
    def ubahHari(self, offset=0):
        today = datetime.today()
        start_of_week = today + timedelta(days=offset * 7)
        return [
            (start_of_week + timedelta(days=i)).strftime("%d/%m/%Y") 
            for i in range(7)
        ]
    
    def BulanSkrngMingguan(self, offset=0):
        today = datetime.today()

        # Hitung bulan dan tahun berdasarkan offset
        year = today.year + (today.month + offset - 1) // 12
        month = (today.month + offset - 1) % 12 + 1

        # Hari pertama dan terakhir di bulan tersebut
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        minggu = []
        current_day = first_day

        while current_day <= last_day:
            # Awal minggu dimulai dari current_day
            week = []
            for i in range(7):
                day = current_day + timedelta(days=i)
                if day.month != month:
                    break
                week.append(day.strftime("%d/%m/%Y"))
            minggu.append(week)
            current_day += timedelta(days=len(week))

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
        if current_month > 6:
            current_month = 12
        else:
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

    def generate_statistics(self, plot_widget):
        try:
            # Cek validitas objek
            if not plot_widget or not hasattr(plot_widget, 'clear'):
                print("Plot widget tidak valid. Skip generate_statistics.")
                return

            plot_widget.clear()

            data = self.generate_data()

            x = data[0]
            income_barItem = data[1]
            outcome_barItem = data[2]
            infoLabels = data[3]
            maxNilai = max(data[1] + data[2]) if data[1] + data[2] else 0

            # Batang pendapatan dan pengeluaran
            income_graph = BarGraphItem(x=x - 0.15, height=income_barItem, width=0.3, brush='g', name="Pendapatan")
            outcome_graph = BarGraphItem(x=x + 0.15, height=outcome_barItem, width=0.3, brush='r', name="Pengeluaran")

            plot_widget.addItem(income_graph)
            plot_widget.addItem(outcome_graph)

            # Label sumbu X
            plot_widget.getAxis('bottom').setTicks([list(zip(x, infoLabels))])
            plot_widget.setLabel('left', 'Nilai')
            plot_widget.setLabel('bottom', 'Hari dan Tanggal')

            # Tampilkan nilai di atas batang
            for i, val in enumerate(income_barItem):
                text = TextItem(str(val), color='black')
                text.setPos(x[i] - 0.25, val + 100)
                plot_widget.addItem(text)

            for i, val in enumerate(outcome_barItem):
                text = TextItem(str(val), color='black')
                text.setPos(x[i], val + 100)
                plot_widget.addItem(text)

            # Label sumbu Y dengan format jelas
            axis = plot_widget.getAxis('left')
            step = max(1, int(maxNilai / 5)) if maxNilai else 1
            ticks = [(i, "{:,.0f}".format(i)) for i in range(0, maxNilai + 1, step)]
            axis.setTicks([ticks])

            # Atur view range
            plot_widget.getPlotItem().vb.setRange(yRange=(0, int(maxNilai * 1.3) if maxNilai else 100), padding=0)
            plot_widget.getPlotItem().hideButtons()
            plot_widget.showGrid(x=True, y=True, alpha=0.3)
            plot_widget.addLegend()

        except RuntimeError as e:
            print(f"[RuntimeError] generate_statistics gagal: {e}")
        except Exception as e:
            print(f"[Exception] generate_statistics gagal: {e}")