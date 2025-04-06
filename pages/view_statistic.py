import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from controller.statistic import Statistic


class StatisticView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.statistic_controller = Statistic()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Membuat plot
        self.plot_widget = pg.PlotWidget()
        # Mengubah latar belakang plot menjadi putih
        self.plot_widget.setBackground('w')
        # Menonaktifkan kemampuan untuk menggeser dan zoom plot
        self.plot_widget.setMouseEnabled(x=False, y=False)
        # Menambahkan plot ke layout
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Plot the graph
        self.generate_statistics()

    def plot_graph(self):
        ax = self.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])  # Sample data
        ax.set_title("Sample Graph")
        self.canvas.draw()

    def generate_statistics(self):
        self.plot_widget.clear()

        data = self.statistic_controller.cur_data

        x = data[0]
        income_barItem = data[1]
        outcome_barItem = data[2]
        infoLabels = data[3]
        maxNilai = max(data[1] + data[2])

        # Membuat grafik batang untuk pendapatan (warna hijau) dan pengeluaran (warna merah)
        income_graph = pg.BarGraphItem(x=x-0.15, height=income_barItem, width=0.3, brush='#FF9F40', name="Pendapatan")
        outcome_graph = pg.BarGraphItem(x=x+0.15, height=outcome_barItem, width=0.3, brush='#F4BE37', name="Pengeluaran")

        # Menambahkan grafik batang ke plot
        self.plot_widget.addItem(income_graph)
        self.plot_widget.addItem(outcome_graph)

        # Mengubah ticks sumbu X untuk menampilkan dua informasi: hari dan tanggal
        self.plot_widget.getAxis('bottom').setTicks([list(zip(x, infoLabels))])

        # Mengubah sumbu Y untuk lebih baik menampilkan data
        self.plot_widget.setLabel('left', 'Nilai')
        self.plot_widget.setLabel('bottom', 'Hari dan Tanggal')

        # Menyesuaikan format label sumbu Y untuk menghindari notasi ilmiah
        axis = self.plot_widget.getAxis('left')
        axis.setTicks([[(i, str(int(i))) for i in range(0, maxNilai, 50000)]])  # Set custom ticks format

        # Tombol untuk mengubah view range setelah beberapa detik
        self.plot_widget.getPlotItem().vb.setRange(yRange=(0, int(maxNilai * 1.2)), padding=0)

        # Menghilangkan toolbar atau elemen lainnya
        self.plot_widget.getPlotItem().hideButtons()  # Menghilangkan tombol atau kontrol lainnya

        # Menambahkan grid pada plot untuk mempermudah pembacaan
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Alpha untuk transparansi grid

        # Menambahkan legenda ke plot
        self.plot_widget.addLegend()  # Ini adalah cara yang benar untuk menambahkan legenda
