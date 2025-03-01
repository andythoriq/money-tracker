from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
import sys
from pages.view_wallet import WalletView
from pages.view_income import IncomeView
from pages.view_outcome import OutcomeView

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Money Tracker - Dashboard")
        # self.setGeometry(100, 100, 400, 300)
        self.setGeometry(300, 300, 600, 500)

        self.stack = QStackedWidget(self)

        # Halaman utama (Dashboard)
        self.main_menu = QWidget()

        # Halaman lainnya (Wallet, Income, Outcome) diberikan akses ke stack
        self.wallet_view = WalletView(self.stack)
        self.income_view = IncomeView()
        self.outcome_view = OutcomeView()

        self.init_main_menu()
        self.stack.addWidget(self.main_menu)  # Index 0 -> Dashboard
        self.stack.addWidget(self.wallet_view)  # Index 1 -> WalletView
        self.stack.addWidget(self.income_view)
        self.stack.addWidget(self.outcome_view)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def init_main_menu(self):
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Money Tracker", self)
        layout.addWidget(self.label)

        self.btn_income = QPushButton("Tambah Income", self)
        self.btn_income.clicked.connect(lambda: self.stack.setCurrentWidget(self.income_view))

        self.btn_outcome = QPushButton("Tambah Outcome", self)
        self.btn_outcome.clicked.connect(lambda: self.stack.setCurrentWidget(self.outcome_view))

        self.btn_wallet = QPushButton("Wallet", self)
        self.btn_wallet.clicked.connect(lambda: self.stack.setCurrentWidget(self.wallet_view))

        layout.addWidget(self.btn_income)
        layout.addWidget(self.btn_outcome)
        layout.addWidget(self.btn_wallet)

        self.main_menu.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
