from pyqtgraph import PlotWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QFrame, QLabel, QComboBox, QPushButton, QSpacerItem, 
                             QSizePolicy)
from PyQt5 import QtCore, QtWidgets
from controller.statistic import Statistic
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure


class StatisticView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.statistic_controller = Statistic()
        self.setupUi()

    def setupUi(self):
        # Main vertical layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)
        
        # Title Section
        self.title_label = QLabel("Statistic")
        self.title_label.setObjectName("titleLabel")
        self.main_layout.addWidget(self.title_label)

        # Create menu option widget
        self.menuOption = QtWidgets.QWidget(self)
        self.menuOption.setObjectName("menuOption")
        
        # Use grid layout for menu option
        self.menuLayout = QGridLayout(self.menuOption)
        self.menuOption.setLayout(self.menuLayout)
        
        # Add menu option to main layout
        self.main_layout.addWidget(self.menuOption)
        
        # Setup plot widget
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setMouseEnabled(x=False, y=False)
        
        # Create top row with Income and Outcome frames
        self.topRowLayout = QHBoxLayout()
        
        # Income frame
        self.Income = QFrame()
        self.Income.setObjectName("QFrameLayout")
        self.Income.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Income.setFrameShadow(QtWidgets.QFrame.Raised)
        self.incomeLayout = QVBoxLayout(self.Income)
        
        self.incomeInfo = QLabel()
        self.incomeInfo.setObjectName("form_label")
        self.incomeInfo.setAlignment(Qt.AlignCenter)
        
        self.IncomeValue = QLabel()
        self.IncomeValue.setObjectName("form_label")
        self.IncomeValue.setAlignment(Qt.AlignCenter)
        
        self.incomeLayout.addWidget(self.incomeInfo)
        self.incomeLayout.addWidget(self.IncomeValue)
        self.topRowLayout.addWidget(self.Income)
        
        # Outcome frame
        self.Outcome = QFrame()
        self.Outcome.setObjectName("QFrameLayout")
        self.Outcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Outcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outcomeLayout = QVBoxLayout(self.Outcome)
        
        self.outcomeInfo = QLabel()
        self.outcomeInfo.setObjectName("form_label")
        self.outcomeInfo.setAlignment(Qt.AlignCenter)
        
        self.outcomeValue = QLabel()
        self.outcomeValue.setObjectName("form_label")
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
        self.Statistic.setObjectName("QFrameLayout")
        self.statisticLayout = QVBoxLayout(self.Statistic)
        
        # Statistic header layout
        self.statisticHeaderLayout = QHBoxLayout()
        
        self.statisticInfo = QLabel()
        self.statisticInfo.setObjectName("form_label")
        self.statisticInfo.setTextFormat(QtCore.Qt.RichText)
        
        self.statisticOption = QComboBox()
        self.statisticOption.setObjectName("iconDesign")
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
        self.prevButton.setObjectName("buttonStyle")
        self.prevButton.setMaximumWidth(40)
        
        self.sliderType = QComboBox()
        self.sliderType.setObjectName("sliderType")
        for _ in range(4):
            self.sliderType.addItem("")
        
        self.nextButton = QPushButton()
        self.nextButton.setObjectName("buttonStyle")
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
        self.pieChart.setObjectName("QFrameLayout")
        self.pieChartLayout = QVBoxLayout(self.pieChart)
        
        # Pie chart header layout
        self.pieChartHeaderLayout = QHBoxLayout()
        
        self.chartInfo = QLabel()
        self.chartInfo.setObjectName("form_label")
        self.chartInfo.setTextFormat(QtCore.Qt.RichText)
        
        self.pieChartOption = QComboBox()
        self.pieChartOption.setObjectName("iconDesign")
        self.pieChartOption.addItem("")
        self.pieChartOption.addItem("")
        
        self.pieChartHeaderLayout.addWidget(self.chartInfo)
        self.pieChartHeaderLayout.addStretch()
        self.pieChartHeaderLayout.addWidget(self.pieChartOption)
        
        # Add pie chart header to pie chart layout
        self.pieChartLayout.addLayout(self.pieChartHeaderLayout)
        
        # Add pie chart placeholder
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.statistic_controller.generate_pie(self.fig)
        self.pieChartLayout.addWidget(self.canvas)
        
        # Add pie chart to right side layout
        self.rightSideLayout.addWidget(self.pieChart)
        
        # Summary frame
        self.Summary = QFrame()
        self.Summary.setObjectName("QFrameLayout")
        self.Summary.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Summary.setFrameShadow(QtWidgets.QFrame.Raised)
        self.summaryLayout = QVBoxLayout(self.Summary)
        
        # Summary header
        self.summaryInfo = QLabel()
        self.summaryInfo.setObjectName("form_label")
        self.summaryInfo.setAlignment(Qt.AlignCenter)
        self.summaryLayout.addWidget(self.summaryInfo)
        
        # Previous balance section
        self.prevBalanceLayout = QVBoxLayout()
        self.prevBalance = QLabel()
        self.prevBalance.setObjectName("form_label")
        self.prevValue = QLabel()
        self.prevValue.setObjectName("form_label")
        self.prevValue.setAlignment(Qt.AlignRight)
        self.prevBalanceLayout.addWidget(self.prevBalance)
        self.prevBalanceLayout.addWidget(self.prevValue)
        
        # Add previous balance to summary layout
        self.summaryLayout.addLayout(self.prevBalanceLayout)
        
        # New balance section
        self.newBalanceLayout = QVBoxLayout()
        self.newBalance = QLabel()
        self.newBalance.setObjectName("form_label")
        self.newValue = QLabel()
        self.newValue.setObjectName("form_label")
        self.newValue.setAlignment(Qt.AlignRight)
        self.newBalanceLayout.addWidget(self.newBalance)
        self.newBalanceLayout.addWidget(self.newValue)
        
        # Add new balance to summary layout
        self.summaryLayout.addLayout(self.newBalanceLayout)
        
        # Change value
        self.changeValueLayout = QHBoxLayout()
        self.changeValue = QLabel()
        self.changeValue.setObjectName("form_label")
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
        self.retranslateUi()
        self.statistic_controller.generate_statistics(self.plot_widget)
        self.update_label()
        
        # Connect signals
        self.sliderType.installEventFilter(self)
        self.sliderType.currentIndexChanged.connect(self.on_combobox_selection_changed)
        self.pieChartOption.currentIndexChanged.connect(self.on_pie_selection_changed)
        self.statisticOption.currentIndexChanged.connect(self.on_bar_selection_changed)
        self.prevButton.clicked.connect(lambda: self.change_offset('prev'))
        self.nextButton.clicked.connect(lambda: self.change_offset('next'))
        self.statisticOption.installEventFilter(self)
        self.pieChartOption.installEventFilter(self)
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def eventFilter(self, obj, event):
        # Memastikan hanya ComboBox yang scroll yang diblokir
        comboBox = [self.statisticOption, self.sliderType, self.pieChartOption]
        if obj in comboBox and event.type() == QtCore.QEvent.Wheel:
            return True  # Mencegah event scroll
        return super().eventFilter(obj, event)

    def on_combobox_selection_changed(self, index):
        selected_item = self.sliderType.currentText()  # Get the text of the selected item
        self.statistic_controller.offset = 0
        # Run specific methods based on the selected item
        if selected_item == "Daily":
            self.statistic_controller.jenis = "harian"
        elif selected_item == "Weekly":
            self.statistic_controller.jenis = "mingguan"
        elif selected_item == "Monthly":
            self.statistic_controller.jenis = "bulanan"
        elif selected_item == "Yearly":
            self.statistic_controller.jenis = "tahunan"
        self.statistic_controller.cur_data = self.statistic_controller.generate_data()
        self.statistic_controller.generate_statistics(self.plot_widget)
        self.statistic_controller.generate_pie(self.fig)
        self.update_label()

    def on_pie_selection_changed(self, index):
        selected_item = self.pieChartOption.currentText()  # Get the current text
        if selected_item == "Save Graphic":
            try:
                # Save the figure as a PNG file
                self.fig.savefig("pie_chart.png", format='png')  # Save as PNG (or choose other formats like 'pdf', 'svg')
                print("Pie chart saved successfully as pie_chart.png")
            except Exception as e:
                print(f"Error saving pie chart: {e}")

    def on_bar_selection_changed(self, index):
        selected_item = self.statisticOption.currentText()  # Get the current text
        if selected_item == "Save Graphic":
            self.statistic_controller.save_graph(self, self.plot_widget)       

    def change_offset(self, direction):
        if direction == 'next':
            self.statistic_controller.offset += 1
        elif direction == 'prev':
            self.statistic_controller.offset -= 1
        self.statistic_controller.cur_data = self.statistic_controller.generate_data()
        self.statistic_controller.generate_statistics(self.plot_widget)
        self.statistic_controller.generate_pie(self.fig)
        self.statistic_controller.update_data(direction)
        self.update_label()

    def update_label(self):
        # Update the text of the QLabel
        self.IncomeValue.setText(str(self.statistic_controller.cur_data[4][0]))
        self.outcomeValue.setText(str(self.statistic_controller.cur_data[4][1]))
        self.prevValue.setText(str(self.statistic_controller.new_balance))
        self.newValue.setText(str(self.statistic_controller.cur_balance))
        self.changeValue.setText(str(self.statistic_controller.net))
        if self.statistic_controller.net < 0:
            self.changeValue.setStyleSheet("color: #FF0000;")
        else:
            self.changeValue.setStyleSheet("color: #00FF00;")

    def retranslateUi(self, lang=None):
        _translate = QtCore.QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("statistic", {}).get("Title", "Statistic")))
            self.incomeInfo.setText(_translate("Form", lang.get("statistic", {}).get("head1", "<html>Jumlah <br>Income</html>")))
            self.outcomeInfo.setText(_translate("Form", lang.get("statistic", {}).get("head2", "<html>Jumlah <br>Outcome</html>")))
            self.statisticInfo.setText(_translate("Form", lang.get("statistic", {}).get("head3", "Statistic")))
            self.chartInfo.setText(_translate("Form", lang.get("statistic", {}).get("head4", "Category Chart")))
            self.summaryInfo.setText(_translate("Form", lang.get("statistic", {}).get("head5", "<html>QuickView <br>Summary<html>")))
            self.newBalance.setText(_translate("Form", lang.get("statistic", {}).get("desc1", "New Balance")))
            self.prevBalance.setText(_translate("Form", lang.get("statistic", {}).get("desc2", "Previous Balance")))

        else:
            self.incomeInfo.setText(_translate("Statistik", "<html>Jumlah <br>Income</html>"))
            self.outcomeInfo.setText(_translate("Statistik", "<html>Jumlah <br>Outcome</html>"))
            
            self.statisticOption.setItemText(0, _translate("Statistik", ""))
            self.statisticOption.setItemText(1, _translate("Statistik", "Save Graphic"))
            
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

            self.pieChartOption.setItemText(0, _translate("Statistik", ""))
            self.pieChartOption.setItemText(1, _translate("Statistik", "Save Graphic"))
            
            self.chartInfo.setText(_translate("Statistik", "Category Chart"))