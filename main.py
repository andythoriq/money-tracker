from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import sys
from pages.income.view_income import IncomeWindow

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Money Tracker - Dashboard")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Welcome to Money Tracker", self)

        self.btn_income = QPushButton("Tambah Income", self)
        self.btn_income.clicked.connect(self.open_income)

        self.btn_outcome = QPushButton("Tambah Outcome", self)
        # self.btn_outcome.clicked.connect()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn_income)
        self.layout.addWidget(self.btn_outcome)

        self.setLayout(self.layout)

    # method untuk masing-masing window
    def open_income(self):
        self.income_window = IncomeWindow()
        self.income_window.show()

    def open_outcome(self):
        pass

    def open_wallet(self):
        pass

    def open_wishlist(self):
        pass

    def open_category(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())