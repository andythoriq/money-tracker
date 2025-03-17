import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
from pages.view_wallet import WalletView
from pages.view_income import IncomeView
from pages.view_outcome import OutcomeView
from pages.view_history import HistoryView
from pages.view_category import CategoryView
from pages.view_wishlist import WishlistView

def load_stylesheet(app, filename="styles/style.qss"):
    with open(filename, "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.center_on_screen()

    def init_ui(self):
        self.setWindowTitle("Money Tracker - Dashboard")

        # self.setGeometry(100, 100, 400, 300)
        self.setGeometry(0, 0, 1600, 900)

        self.stack = QStackedWidget(self)
        

        # Halaman utama (Dashboard)
        self.main_menu = QWidget()

        # Halaman lainnya
        self.wallet_view = WalletView(self.stack)
        self.income_view = IncomeView(self.stack)
        self.outcome_view = OutcomeView(self.stack)
        self.history_view = HistoryView(self.stack)
        self.category_view = CategoryView(self.stack)
        self.wishlist_view = WishlistView(self.stack)

        self.init_main_menu()
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.wallet_view)
        self.stack.addWidget(self.income_view)
        self.stack.addWidget(self.outcome_view)
        self.stack.addWidget(self.history_view)
        self.stack.addWidget(self.category_view)
        self.stack.addWidget(self.wishlist_view)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def init_main_menu(self):
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to Money Tracker", self)
        layout.addWidget(self.label)

        self.income = QPushButton("Tambah Income", self)
        self.income.clicked.connect(lambda: (
            self.income_view.refresh_combobox(),
            self.stack.setCurrentWidget(self.income_view)
        ))

        self.outcome = QPushButton("Tambah Outcome", self)
        self.outcome.clicked.connect(lambda: (
            self.outcome_view.refresh_combobox(), 
            self.stack.setCurrentWidget(self.outcome_view)
        ))

        self.history = QPushButton("History Transaksi", self)
        self.history.clicked.connect(lambda: (
            self.history_view.load_data("all"),
            self.history_view.radio_all.setChecked(True),
            self.stack.setCurrentWidget(self.history_view)
        ))

        self.wallet = QPushButton("Wallet", self)
        self.wallet.clicked.connect(lambda: (
            self.wallet_view.load_wallets(),
            self.stack.setCurrentWidget(self.wallet_view)
        ))

        self.category = QPushButton("Manage Categories")
        self.category.clicked.connect(lambda: self.stack.setCurrentWidget(self.category_view))

        self.btn_wishlist = QPushButton("Wish Lists")
        self.btn_wishlist.clicked.connect(lambda: (
            self.wishlist_view.load_wishlists(),
            self.wishlist_view.all_status.setChecked(True),
            self.stack.setCurrentWidget(self.wishlist_view),
        ))

        layout.addWidget(self.btn_income)
        layout.addWidget(self.btn_outcome)
        layout.addWidget(self.btn_history)
        layout.addWidget(self.btn_wallet)
        layout.addWidget(self.btn_category)
        layout.addWidget(self.btn_wishlist)

        self.main_menu.setLayout(layout)

    def center_on_screen(self):
        """Memusatkan jendela di tengah layar."""
        screen = QApplication.primaryScreen().geometry()
        win_rect = self.frameGeometry()
        x = (screen.width() - win_rect.width()) // 2
        y = (screen.height() - win_rect.height()) // 2
        self.move(x, y)