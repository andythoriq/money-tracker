from pyqtgraph import TextItem, PlotWidget, BarGraphItem
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QFrame, QLabel, QComboBox, QPushButton, QSpacerItem, 
                             QSizePolicy)
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

    def setupUi(self):
        # Main vertical layout
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)
        
        # Create menu option widget
        self.menuOption = QtWidgets.QWidget(self)
        self.menuOption.setObjectName("menuOption")
        
        # Use grid layout for menu option
        self.menuLayout = QGridLayout(self.menuOption)
        self.menuOption.setLayout(self.menuLayout)
        
        # Add menu option to main layout
        self.mainLayout.addWidget(self.menuOption)
        
        # Setup plot widget
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setMouseEnabled(x=False, y=False)
        
        # Create top row with Income and Outcome frames
        self.topRowLayout = QHBoxLayout()
        
        # Income frame
        self.Income = QFrame()
        self.Income.setObjectName("Income")
        self.Income.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Income.setFrameShadow(QtWidgets.QFrame.Raised)
        self.incomeLayout = QVBoxLayout(self.Income)
        
        self.incomeInfo = QLabel()
        self.incomeInfo.setObjectName("incomeInfo")
        self.incomeInfo.setAlignment(Qt.AlignCenter)
        
        self.IncomeValue = QLabel()
        self.IncomeValue.setObjectName("IncomeValue")
        self.IncomeValue.setAlignment(Qt.AlignCenter)
        
        self.incomeLayout.addWidget(self.incomeInfo)
        self.incomeLayout.addWidget(self.IncomeValue)
        self.topRowLayout.addWidget(self.Income)
        
        # Outcome frame
        self.Outcome = QFrame()
        self.Outcome.setObjectName("Outcome")
        self.Outcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Outcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outcomeLayout = QVBoxLayout(self.Outcome)
        
        self.outcomeInfo = QLabel()
        self.outcomeInfo.setObjectName("outcomeInfo")
        self.outcomeInfo.setAlignment(Qt.AlignCenter)
        
        self.outcomeValue = QLabel()
        self.outcomeValue.setObjectName("outcomeValue")
        self.outcomeValue.setAlignment(Qt.AlignCenter)
        
        self.outcomeLayout.addWidget(self.outcomeInfo)
        self.outcomeLayout.addWidget(self.outcomeValue)
        self.topRowLayout.addWidget(self.Outcome)
        
        # Add top row to menu layout
        self.menuLayout.addLayout(self.topRowLayout, 0, 0, 1, 1)
        
        # Create middle section with Statistics and Chart
        self.middleRowLayout = QHBoxLayout()
        
        # Statistics frame
        self.Statistic = QFrame()
        self.Statistic.setObjectName("Statistic")
        self.statisticLayout = QVBoxLayout(self.Statistic)
        
        # Statistic header layout
        self.statisticHeaderLayout = QHBoxLayout()
        
        self.statisticInfo = QLabel()
        self.statisticInfo.setObjectName("statisticInfo")
        self.statisticInfo.setTextFormat(QtCore.Qt.RichText)
        
        self.statisticOption = QComboBox()
        self.statisticOption.setObjectName("statisticOption")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")
        self.statisticOption.addItem("")  # separator
        self.statisticOption.addItem("")
        
        self.statisticHeaderLayout.addWidget(self.statisticInfo)
        self.statisticHeaderLayout.addStretch()
        self.statisticHeaderLayout.addWidget(self.statisticOption)
        
        # Add statistic header to statistic layout
        self.statisticLayout.addLayout(self.statisticHeaderLayout)
        
        # Slider button widget
        self.sliderLayout = QHBoxLayout()
        
        self.prevButton = QPushButton()
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setMaximumWidth(40)
        
        self.sliderType = QComboBox()
        self.sliderType.setObjectName("sliderType")
        self.sliderType.addItem("")
        self.sliderType.addItem("")
        self.sliderType.addItem("")
        self.sliderType.addItem("")
        
        self.nextButton = QPushButton()
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setMaximumWidth(40)
        
        self.sliderLayout.addStretch()
        self.sliderLayout.addWidget(self.prevButton)
        self.sliderLayout.addWidget(self.sliderType)
        self.sliderLayout.addWidget(self.nextButton)
        self.sliderLayout.addStretch()
        
        # Add slider layout to statistic layout
        self.statisticLayout.addLayout(self.sliderLayout)
        
        # Bar chart layout
        self.barChartLayout = QVBoxLayout()
        self.barChartLayout.addWidget(self.plot_widget)
        
        # Add bar chart to statistic layout
        self.statisticLayout.addLayout(self.barChartLayout)
        
        # Add statistic frame to middle row
        self.middleRowLayout.addWidget(self.Statistic, 3)
        
        # Right side layout (pie chart and summary)
        self.rightSideLayout = QVBoxLayout()
        
        # Pie chart frame
        self.pieChart = QFrame()
        self.pieChart.setObjectName("pieChart")
        self.pieChartLayout = QVBoxLayout(self.pieChart)
        
        # Pie chart header layout
        self.pieChartHeaderLayout = QHBoxLayout()
        
        self.chartInfo = QLabel()
        self.chartInfo.setObjectName("chartInfo")
        self.chartInfo.setTextFormat(QtCore.Qt.RichText)
        
        self.pieChartOption = QComboBox()
        self.pieChartOption.setObjectName("pieChartOption")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        
        self.pieChartHeaderLayout.addWidget(self.chartInfo)
        self.pieChartHeaderLayout.addStretch()
        self.pieChartHeaderLayout.addWidget(self.pieChartOption)
        
        # Add pie chart header to pie chart layout
        self.pieChartLayout.addLayout(self.pieChartHeaderLayout)
        
        # Add pie chart placeholder
        self.pieChartPlaceholder = QLabel("Pie Chart Placeholder")
        self.pieChartPlaceholder.setAlignment(Qt.AlignCenter)
        self.pieChartLayout.addWidget(self.pieChartPlaceholder)
        
        # Add pie chart to right side layout
        self.rightSideLayout.addWidget(self.pieChart)
        
        # Summary frame
        self.Summary = QFrame()
        self.Summary.setObjectName("Summary")
        self.Summary.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Summary.setFrameShadow(QtWidgets.QFrame.Raised)
        self.summaryLayout = QVBoxLayout(self.Summary)
        
        # Summary header
        self.summaryInfo = QLabel()
        self.summaryInfo.setObjectName("summaryInfo")
        self.summaryInfo.setAlignment(Qt.AlignCenter)
        self.summaryLayout.addWidget(self.summaryInfo)
        
        # Previous balance section
        self.prevBalanceLayout = QVBoxLayout()
        self.prevBalance = QLabel()
        self.prevBalance.setObjectName("prevBalance")
        self.prevValue = QLabel()
        self.prevValue.setObjectName("prevValue")
        self.prevValue.setAlignment(Qt.AlignRight)
        self.prevBalanceLayout.addWidget(self.prevBalance)
        self.prevBalanceLayout.addWidget(self.prevValue)
        
        # Add previous balance to summary layout
        self.summaryLayout.addLayout(self.prevBalanceLayout)
        
        # New balance section
        self.newBalanceLayout = QVBoxLayout()
        self.newBalance = QLabel()
        self.newBalance.setObjectName("newBalance")
        self.newValue = QLabel()
        self.newValue.setObjectName("newValue")
        self.newValue.setAlignment(Qt.AlignRight)
        self.newBalanceLayout.addWidget(self.newBalance)
        self.newBalanceLayout.addWidget(self.newValue)
        
        # Add new balance to summary layout
        self.summaryLayout.addLayout(self.newBalanceLayout)
        
        # Change value
        self.changeValueLayout = QHBoxLayout()
        self.changeValue = QLabel()
        self.changeValue.setObjectName("changeValue")
        self.changeValue.setAlignment(Qt.AlignCenter)
        self.changeValueLayout.addStretch()
        self.changeValueLayout.addWidget(self.changeValue)
        self.changeValueLayout.addStretch()
        
        # Add change value to summary layout
        self.summaryLayout.addLayout(self.changeValueLayout)
        
        # Add summary to right side layout
        self.rightSideLayout.addWidget(self.Summary)
        
        # Add right side layout to middle row
        self.middleRowLayout.addLayout(self.rightSideLayout, 2)
        
        # Add middle row to menu layout
        self.menuLayout.addLayout(self.middleRowLayout, 1, 0, 1, 1)
        
        # Set up event handlers and UI elements
        self.retranslateUi(self)
        self.styleSheet(self)
        self.generate_statistics()
        
        # Connect signals
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

        buttonStyle = """
            QPushButton {
                background-color: #D3D3D3;
                border-radius: 10px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A9A9A9;
            }
        """

        Statistik.setStyleSheet("background-color: #252931;")

        self.incomeInfo.setStyleSheet(textDesign)
        self.outcomeInfo.setStyleSheet(textDesign)
        self.summaryInfo.setStyleSheet(textDesign)

        self.IncomeValue.setStyleSheet(textDesign)
        self.outcomeValue.setStyleSheet(textDesign)

        self.prevBalance.setStyleSheet(textDesign)
        self.newBalance.setStyleSheet(textDesign)

        self.prevValue.setStyleSheet(textDesign)
        self.newValue.setStyleSheet(textDesign)

        self.changeValue.setStyleSheet(textDesign)
        
        '''
        if -:
            self.changeValue.setStyleSheet("color: #FF0000;")
        elif +:
            self.changeValue.setStyleSheet("color: #00FF00;")
        '''

        self.Statistic.setStyleSheet(chartDesign)
        self.prevButton.setStyleSheet(buttonStyle)
        self.nextButton.setStyleSheet(buttonStyle)
        self.sliderType.setStyleSheet("background-color: #D3D3D3; padding: 5px; border-radius: 5px;")
        self.pieChart.setStyleSheet(chartDesign)

        self.statisticInfo.setStyleSheet(StatistikDesign)
        self.chartInfo.setStyleSheet(StatistikDesign)

        self.Summary.setStyleSheet(frameDesign)
        self.Income.setStyleSheet(frameDesign)
        self.Outcome.setStyleSheet(frameDesign)

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