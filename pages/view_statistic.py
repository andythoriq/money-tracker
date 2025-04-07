from pyqtgraph import TextItem, PlotWidget, BarGraphItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5 import QtCore, QtWidgets
from controller.statistic import Statistic
from PyQt5.QtCore import Qt


class StatisticView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.statistic_controller = Statistic()
        self.offset = 0
        self.jenis = ""
        self.setupUi()

    def init_ui(self):
        self.statistic_controller = Statistic()
        layout = QVBoxLayout()
        # Membuat plot
        self.plot_widget = PlotWidget()
        # Mengubah latar belakang plot menjadi putih
        self.plot_widget.setBackground('w')
        # Menonaktifkan kemampuan untuk menggeser dan zoom plot
        self.plot_widget.setMouseEnabled(x=False, y=False)
        # Menambahkan plot ke layout
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Plot the graph
        self.generate_statistics()

    def setupUi(self):
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setMouseEnabled(x=False, y=False)

        self.menuOption = QtWidgets.QWidget(self)
        self.menuOption.setObjectName("menuOption")
        
        self.Income = QtWidgets.QFrame(self.menuOption)
        self.Income.setGeometry(QtCore.QRect(30, 20, 342, 222))
        self.Income.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Income.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Income.setObjectName("Income")
        
        self.incomeInfo = QtWidgets.QLabel(self.Income)
        self.incomeInfo.setGeometry(QtCore.QRect(40, 40, 200, 90))
        self.incomeInfo.setObjectName("incomeInfo")
        
        self.IncomeValue = QtWidgets.QLabel(self.Income)
        self.IncomeValue.setGeometry(QtCore.QRect(60, 140, 162, 32))
        self.IncomeValue.setObjectName("IncomeValue")
        
        self.Outcome = QtWidgets.QFrame(self.menuOption)
        self.Outcome.setGeometry(QtCore.QRect(400, 20, 342, 222))
        self.Outcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Outcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Outcome.setObjectName("Outcome")
        
        self.outcomeInfo = QtWidgets.QLabel(self.Outcome)
        self.outcomeInfo.setGeometry(QtCore.QRect(40, 40, 200, 90))
        self.outcomeInfo.setObjectName("outcomeInfo")

        self.outcomeValue = QtWidgets.QLabel(self.Outcome)
        self.outcomeValue.setGeometry(QtCore.QRect(80, 140, 162, 32))
        self.outcomeValue.setObjectName("outcomeValue")
        
        self.Statistic = QtWidgets.QFrame(self.menuOption)
        self.Statistic.setGeometry(QtCore.QRect(30, 260, 722, 602))
        self.Statistic.setObjectName("Statistic")
        
        self.statisticOption = QtWidgets.QComboBox(self.menuOption)
        self.statisticOption.setGeometry(QtCore.QRect(680, 280, 60, 44))
        self.statisticOption.setObjectName("statisticOption")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")  # separator
        self.statisticOption.addItem("")
        
        self.SliderButton = QtWidgets.QWidget(self.Statistic)
        self.SliderButton.setGeometry(QtCore.QRect(420, 20, 222, 42))
        self.SliderButton.setObjectName("SliderButton")
        
        self.prevButton = QtWidgets.QPushButton(self.SliderButton)
        self.prevButton.setGeometry(QtCore.QRect(0, 0, 42, 46))
        self.prevButton.setObjectName("prevButton")
        
        self.nextButton = QtWidgets.QPushButton(self.SliderButton)
        self.nextButton.setGeometry(QtCore.QRect(180, 0, 40, 46))
        self.nextButton.setObjectName("nextButton")

        self.sliderType = QtWidgets.QComboBox(self.SliderButton)
        self.sliderType.setGeometry(QtCore.QRect(40, 0, 138, 44))
        self.sliderType.setObjectName("sliderType")
        self.sliderType.addItem("")
        self.sliderType.addItem("")
        self.sliderType.addItem("")
        self.sliderType.addItem("")

        self.statisticInfo = QtWidgets.QLabel(self.menuOption)
        self.statisticInfo.setGeometry(QtCore.QRect(70, 300, 180, 60))
        self.statisticInfo.setTextFormat(QtCore.Qt.RichText)
        self.statisticInfo.setObjectName("statisticInfo")
        
        self.barChart = QtWidgets.QWidget(self.menuOption)
        self.barChart.setGeometry(QtCore.QRect(50, 360, 682, 502))
        self.barChart.setObjectName("barChart")
        self.graph = QtWidgets.QVBoxLayout(self.barChart)
        self.graph.addWidget(self.plot_widget)
        
        self.timeInfo = QtWidgets.QLabel(self.Statistic)
        self.timeInfo.setGeometry(QtCore.QRect(300, 100, 94, 26))
        self.timeInfo.setTextFormat(QtCore.Qt.RichText)
        self.timeInfo.setObjectName("timeInfo")
        
        self.pieChart = QtWidgets.QFrame(self.menuOption)
        self.pieChart.setGeometry(QtCore.QRect(770, 20, 462, 422))
        self.pieChart.setObjectName("pieChart")
        
        self.chartInfo = QtWidgets.QLabel(self.menuOption)
        self.chartInfo.setGeometry(QtCore.QRect(830, 40, 320, 60))
        self.chartInfo.setTextFormat(QtCore.Qt.RichText)
        self.chartInfo.setObjectName("chartInfo")

        self.pieChartOption = QtWidgets.QComboBox(self.menuOption)
        self.pieChartOption.setGeometry(QtCore.QRect(1140, 50, 60, 44))
        self.pieChartOption.setObjectName("pieChartOption")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")

        self.Summary = QtWidgets.QFrame(self.menuOption)
        self.Summary.setGeometry(QtCore.QRect(770, 460, 458, 412))
        self.Summary.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Summary.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Summary.setObjectName("Summary")
        
        self.summaryInfo = QtWidgets.QLabel(self.Summary)
        self.summaryInfo.setGeometry(QtCore.QRect(80, 20, 300, 80))
        self.summaryInfo.setObjectName("summaryInfo")
        
        self.newBalance = QtWidgets.QLabel(self.Summary)
        self.newBalance.setGeometry(QtCore.QRect(40, 240, 240, 80))
        self.newBalance.setObjectName("newBalance")
        
        self.prevBalance = QtWidgets.QLabel(self.Summary)
        self.prevBalance.setGeometry(QtCore.QRect(40, 120, 280, 80))
        self.prevBalance.setObjectName("prevBalance")
        
        self.prevValue = QtWidgets.QLabel(self.Summary)
        self.prevValue.setGeometry(QtCore.QRect(40, 180, 340, 32))
        self.prevValue.setObjectName("prevValue")
        
        self.newValue = QtWidgets.QLabel(self.Summary)
        self.newValue.setGeometry(QtCore.QRect(40, 300, 340, 32))
        self.newValue.setObjectName("newValue")
        
        self.changeValue = QtWidgets.QLabel(self.Summary)
        self.changeValue.setGeometry(QtCore.QRect(180, 360, 142, 32))
        self.changeValue.setObjectName("changeValue")
        
        self.retranslateUi(self)
        self.styleSheet(self)
        self.generate_statistics()
        self.sliderType.installEventFilter(self)
        self.sliderType.currentIndexChanged.connect(self.on_combobox_selection_changed)
        self.prevButton.clicked.connect(lambda: self.change_offset('prev'))
        self.nextButton.clicked.connect(lambda: self.change_offset('next'))
        self.statisticOption.installEventFilter(self)
        self.pieChartOption.installEventFilter(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Statistik):
        _translate = QtCore.QCoreApplication.translate
        Statistik.setWindowTitle(_translate("Statistik", "MainWindow"))
        
        self.incomeInfo.setText(_translate("Statistik", "<html>Jumlah <br>Income</html>"))
        self.IncomeValue.setText(_translate("Statistik", str(self.statistic_controller.cur_data[4])))
        self.outcomeInfo.setText(_translate("Statistik", "<html>Jumlah <br>Outcome</html>"))
        self.outcomeValue.setText(_translate("Statistik", str(self.statistic_controller.cur_data[5])))
        
        self.statisticOption.setItemText(0, _translate("Statistik", "by day"))
        self.statisticOption.setItemText(1, _translate("Statistik", "by week"))
        self.statisticOption.setItemText(2, _translate("Statistik", "by month"))
        self.statisticOption.setItemText(3, _translate("Statistik", "by year"))
        self.statisticOption.setItemText(4, _translate("Statistik", "~~~~~~~"))
        self.statisticOption.setItemText(5, _translate("Statistik", "Save Graphic"))
        
        self.prevButton.setText(_translate("Statistik", "<"))
        self.nextButton.setText(_translate("Statistik", ">"))
        
        self.sliderType.setItemText(0, _translate("Statistik", "Daily"))
        self.sliderType.setItemText(1, _translate("Statistik", "Weekly"))
        self.sliderType.setItemText(2, _translate("Statistik", "Monthly"))
        self.sliderType.setItemText(3, _translate("Statistik", "Yearly"))
        
        self.statisticInfo.setText(_translate("Statistik", "Statistic"))
        self.timeInfo.setText(_translate("Statistik", "Statistic"))
        self.summaryInfo.setText(_translate("Statistik", "<html>QuickView <br>Summary<html>"))
        self.newBalance.setText(_translate("Statistik", "New Balance"))
        self.prevBalance.setText(_translate("Statistik", "Previous Balance"))
        self.prevValue.setText(_translate("Statistik", "Rp. X00.000"))
        self.newValue.setText(_translate("Statistik", "Rp. X00.000"))
        self.changeValue.setText(_translate("Statistik", "+Rp. X0.000"))
        
        self.pieChartOption.setItemText(0, _translate("Statistik", "by Income"))
        self.pieChartOption.setItemText(1, _translate("Statistik", "by Outcome"))
        self.pieChartOption.setItemText(2, _translate("Statistik", "~~~~~~~~"))
        self.pieChartOption.setItemText(3, _translate("Statistik", "Save Graphic"))
        
        self.chartInfo.setText(_translate("Statistik", "Category Chart"))

    def styleSheet(self, Statistik):
        iconDesign = """
            QComboBox {
                background-color: transparent;
                width: 60px;  /* Only the width for the dropdown arrow */
                height: 22px;
                padding: 0px;
                border: none;  /* Remove border */
                text-align: center;  /* Ensure nothing is visible in collapsed state */
            }

            QComboBox::drop-down {
                width: 60px;  /* Size of the dropdown arrow */
            }

            QComboBox::down-arrow {
                image: url(img/icon/database.svg);  /* Ensure this image exists and is correctly loaded */
                width: 60px;  /* Size of the dropdown arrow */
                height: 60px;
            }

            /* Hide the text area but don't completely remove it */
            QComboBox::lineEdit {
                border: none;
                background: transparent;
                padding: 100px;
                color: transparent;  /* Keep the text hidden */
            }

            /* Display dropdown list items correctly */
            QComboBox QAbstractItemView {
                min-width: 150px;  /* Minimum width for dropdown items */
                max-width: 300px;  /* Ensure items have sufficient width to show full text */
                font-size: 14px;
                padding: 100px;
            }

            QComboBox QAbstractItemView::item {
                padding-left: 10px;  /* Indentation for item text */
                padding-right: 10px;
                height: 40px;  /* Height of each item */
            }

            QComboBox::item:selected {
                background-color: lightblue;  /* Background when an item is selected */
                color: black;  /* Text color for selected item */
            }

            QComboBox::editable {
                background: transparent;
                border: none;
                padding: 0px;
                color: transparent;  /* Hide the text but still keep the arrow visible */
            }
        """
        
        textDesign = """
            QLabel {
            font-family: 'Arimo';
            font-size: 16px;             /* Sets font size */
            color: #FFFFFF;                 /* Sets text color */
            font-weight: bold;               /* Makes the font extra bold */
            text-align: center;
             border: none;
            }

            #changeValue {
            font-family: 'Arimo';
            font-size: 10px;             /* Sets font size */
            color: #FFFFFF;                 /* Sets text color */
            font-weight: bold;               /* Makes the font extra bold */
            }
        """

        chartDesign = """
            QFrame    {
            border: 10px solid #191D24; 
            padding: 20px; 
            background-color: #FFFFFF;
            border-radius: 15px; 
            }
        """

        frameDesign = """
            QFrame    {
            background-color: #90B774;
            border-radius: 15px; 
            border: 1px solid #7A9E5D; /* Optional: Adds a border with a slightly darker green */
            }
        """
        
        StatistikDesign = """
            QLabel {    
            font-family: 'Arimo';
            font-size: 20px;
            font-weight: bold;
            color: #E06C75;
            background-color: transparent;
            }
        """

        Statistik.setStyleSheet("background-color: #252931;")

        self.incomeInfo.setStyleSheet(textDesign)
        self.outcomeInfo.setStyleSheet(textDesign)
        self.summaryInfo.setStyleSheet(textDesign)
        self.incomeInfo.setAlignment(Qt.AlignCenter)
        self.outcomeInfo.setAlignment(Qt.AlignCenter)
        self.summaryInfo.setAlignment(Qt.AlignCenter)

        self.IncomeValue.setStyleSheet(textDesign)
        self.outcomeValue.setStyleSheet(textDesign)

        self.prevBalance.setStyleSheet(textDesign)
        self.newBalance.setStyleSheet(textDesign)

        self.prevValue.setStyleSheet(textDesign)
        self.newValue.setStyleSheet(textDesign)
        self.prevValue.setAlignment(Qt.AlignRight)
        self.newValue.setAlignment(Qt.AlignRight)

        self.changeValue.setStyleSheet(textDesign)
        
        '''
        if -:
            self.changeValue.setStyleSheet("color: #FF0000;")
        elif +:
            self.changeValue.setStyleSheet("color: #00FF00;")
        '''

        self.Statistic.setStyleSheet(chartDesign)
        self.SliderButton.setStyleSheet("background-color: #252931;")
        self.barChart.setStyleSheet("background-color: transparent;")
        self.pieChart.setStyleSheet(chartDesign)

        self.statisticInfo.setStyleSheet(StatistikDesign)
        self.chartInfo.setStyleSheet(StatistikDesign)

        self.Summary.setStyleSheet(frameDesign)
        self.Income.setStyleSheet(frameDesign)
        self.Outcome.setStyleSheet(frameDesign)

        self.SliderButton.setStyleSheet("background-color: #D3D3D3;")
        self.statisticOption.setStyleSheet(iconDesign)
        self.pieChartOption.setStyleSheet(iconDesign)

    def eventFilter(self, obj, event):
        # Memastikan hanya ComboBox yang scroll yang diblokir
        comboBox = [self.statisticOption, self.sliderType, self.pieChartOption]
        if obj in comboBox and event.type() == QtCore.QEvent.Wheel:
            return True  # Mencegah event scroll
        return super().eventFilter(obj, event)

    def generate_statistics(self):
        self.plot_widget.clear()

        data = self.statistic_controller.cur_data

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

    def on_combobox_selection_changed(self, index):
        selected_item = self.sliderType.currentText()  # Get the text of the selected item
        self.offset = 0
        # Run specific methods based on the selected item
        if selected_item == "Daily":
            self.jenis = "harian"
        elif selected_item == "Weekly":
            self.jenis = "mingguan"
        elif selected_item == "Monthly":
            self.jenis = "bulanan"
        elif selected_item == "Yearly":
            self.jenis = "tahunan"
        self.statistic_controller.cur_data = self.statistic_controller.generate_data(self.offset, self.jenis)
        self.generate_statistics()

    def change_offset(self, direction):
        if direction == 'next':
            self.offset += 1
        elif direction == 'prev':
            self.offset -= 1
        self.statistic_controller.cur_data = self.statistic_controller.generate_data(self.offset, self.jenis)
        self.generate_statistics()