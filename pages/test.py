import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class IncomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("This is the Income View")
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainMenu(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("This is the Main Menu")
        layout.addWidget(self.label)

        self.btn_edit_income = QPushButton("Edit Income")
        self.btn_edit_income.clicked.connect(self.switch_to_income_view)
        layout.addWidget(self.btn_edit_income)

        self.setLayout(layout)

    def switch_to_income_view(self):
        self.stacked_widget.setCurrentIndex(1)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.stacked_widget = QStackedWidget()

        self.main_menu = MainMenu(self.stacked_widget)
        self.income_view = IncomeView()

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.income_view)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())