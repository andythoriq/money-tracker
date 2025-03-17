import os
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QGroupBox, QHBoxLayout
from PyQt5 import QtGui, QtCore, QtWidgets
from pages.view_wallet import WalletView
from pages.view_income import IncomeView
from pages.view_outcome import OutcomeView
from pages.view_history import HistoryView
from pages.view_category import CategoryView
from pages.view_wishlist import WishlistView
from controller.Popup import PopupAboutUs

def load_stylesheet(app, filename="styles/styleQWidget.qss"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            qss = file.read()
            app.setStyleSheet(qss)
    else:
        print(f"Warning: Stylesheet {filename} not found!")

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1600, 900)  # Ukuran awal jendela

    def init_ui(self):
        """Inisialisasi tampilan UI utama"""
        self.setWindowTitle("Money Tracker")

        # Stack untuk menyimpan berbagai halaman
        self.stack = QStackedWidget()

        # Halaman utama (Dashboard)
        self.main_menu = QWidget()

        # Inisialisasi view-view lainnya
        self.wallet_view = WalletView(self.stack)
        self.income_view = IncomeView(self.stack)
        self.outcome_view = OutcomeView(self.stack)
        self.history_view = HistoryView(self.stack)
        self.category_view = CategoryView(self.stack)
        self.wishlist_view = WishlistView(self.stack)

        # Menambahkan halaman ke stack
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.wallet_view)
        self.stack.addWidget(self.income_view)
        self.stack.addWidget(self.outcome_view)
        self.stack.addWidget(self.history_view)
        self.stack.addWidget(self.category_view)
        self.stack.addWidget(self.wishlist_view)

        # Inisialisasi tampilan utama
        self.init_main_menu()

        # Layout utama
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.HomeSection, 1)  # Sidebar kiri (20%)
        main_layout.addWidget(self.stack, 3)  # Konten utama (80%)
        self.setLayout(main_layout)

    def init_main_menu(self):
        """Inisialisasi tampilan sidebar dan konten utama"""
        self.container = QGroupBox()
        self.container.setObjectName("container")
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.container.setMaximumWidth(1253)  # Batasi lebar konten utama

        self.layout_1 = QGroupBox(self.container)

        self.layout_2 = QGroupBox(self.container)

        self.layout_3 = QGroupBox(self.container)

        self.layout_4 = QGroupBox(self.container)


        self.HomeSection = QGroupBox()
        self.HomeSection.setObjectName("HomeSection")
        self.HomeSection.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.HomeSection.setMaximumWidth(347)  # Batasi lebar sidebar

        # Tombol-tombol Sidebar (HomeSection)
        self.btn_home = QPushButton(self.HomeSection)
        self.btn_home.setIcon(QtGui.QIcon("../money-tracker/img/icon/logo-app.png"))
        self.btn_home.setIconSize(QtCore.QSize(80, 80))
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))
        self.btn_home.setObjectName("btn_home")

        self.btn_income = QPushButton(self.HomeSection)
        self.btn_income.setIcon(QtGui.QIcon("../money-tracker/img/icon/add-income.png"))
        self.btn_income.setIconSize(QtCore.QSize(55, 61))
        self.btn_income.clicked.connect(lambda: (
            self.income_view.refresh_combobox(),
            self.stack.setCurrentWidget(self.income_view),
        ))
        self.btn_income.setObjectName("btn_homeSection")

        self.btn_outcome = QPushButton(self.HomeSection)
        self.btn_outcome.setIcon(QtGui.QIcon("../money-tracker/img/icon/add-outcome.png"))
        self.btn_outcome.setIconSize(QtCore.QSize(55, 61))
        self.btn_outcome.clicked.connect(lambda: (
            self.outcome_view.refresh_combobox(),
            self.stack.setCurrentWidget(self.outcome_view),
        ))
        self.btn_outcome.setObjectName("btn_homeSection")

        self.btn_wallet = QPushButton(self.HomeSection)
        self.btn_wallet.setIcon(QtGui.QIcon("../money-tracker/img/icon/wallet.png"))
        self.btn_wallet.setIconSize(QtCore.QSize(55, 61))
        self.btn_wallet.clicked.connect(lambda: (
            self.wallet_view.load_wallets(),
            self.stack.setCurrentWidget(self.wallet_view),
        ))
        self.btn_wallet.setObjectName("btn_homeSection")

        self.btn_history = QPushButton(self.HomeSection)
        self.btn_history.setIcon(QtGui.QIcon("../money-tracker/img/icon/history.png"))
        self.btn_history.setIconSize(QtCore.QSize(55, 61))
        self.btn_history.clicked.connect(lambda: (
            self.history_view.load_data("all"),
            self.history_view.radio_all.setChecked(True),
            self.stack.setCurrentWidget(self.history_view),
        ))
        self.btn_history.setObjectName("btn_homeSection")

        self.btn_statistic = QPushButton(self.HomeSection)
        self.btn_statistic.setIcon(QtGui.QIcon("../money-tracker/img/icon/statistic.png"))
        self.btn_statistic.setIconSize(QtCore.QSize(55, 61))
        self.btn_statistic.setObjectName("btn_homeSection")

        self.btn_category = QPushButton(self.HomeSection)
        self.btn_category.setIcon(QtGui.QIcon("../money-tracker/img/icon/category.png"))
        self.btn_category.setIconSize(QtCore.QSize(55, 61))
        self.btn_category.clicked.connect(lambda: self.stack.setCurrentWidget(self.category_view))
        self.btn_category.setObjectName("btn_homeSection")

        self.btn_wishlist = QPushButton(self.HomeSection)
        self.btn_wishlist.setIcon(QtGui.QIcon("../money-tracker/img/icon/wishlist.png"))
        self.btn_wishlist.setIconSize(QtCore.QSize(55, 61))
        self.btn_wishlist.clicked.connect(lambda: (
            self.wishlist_view.load_wishlists(),
            self.wishlist_view.all_status.setChecked(True),
            self.stack.setCurrentWidget(self.wishlist_view),
        ))
        self.btn_wishlist.setObjectName("btn_homeSection")

        self.aboutUs = QPushButton(self.HomeSection)
        self.aboutUs.setIcon(QtGui.QIcon("../money-tracker/img/icon/aboutUs.png"))
        self.aboutUs.setIconSize(QtCore.QSize(55, 61))
        self.aboutUs.setStyleSheet("background-color: #121D2C;")
        self.aboutUs.setObjectName("btn_aboutUs")
        self.aboutUs.clicked.connect(lambda: PopupAboutUs(self.aboutUs))

        self.label = QLabel(self.HomeSection)
        self.label.setStyleSheet("color: white; background-color: #121D2C;")
        self.label.setObjectName("label")

        self.retranslateUi()


        # Atur ulang posisi dan ukuran tombol saat pertama kali dijalankan
        self.update_button_geometry()

    def resizeEvent(self, event):
        """Override resizeEvent untuk menyesuaikan ukuran dan posisi tombol"""
        super().resizeEvent(event)
        self.update_button_geometry()

    def update_button_geometry(self):
        """Menghitung ulang posisi dan ukuran tombol berdasarkan ukuran jendela"""
        # Dapatkan ukuran HomeSection
        home_section_width = self.HomeSection.width()
        home_section_height = self.HomeSection.height()

        # Atur ukuran dan posisi tombol
        button_width = int(290)
        button_height = int(76)
        button_logo_height = int(150) # Khusus untuk tombol logo app
        margin = 12  # Jarak antar tombol

        # Posisi awal tombol
        y_position = 20

        # Atur ulang posisi dan ukuran tombol
        self.btn_home.setGeometry(
            int((home_section_width - button_width) / 2),  # Tengah horizontal
            y_position,
            button_width,
            button_logo_height
        )
        y_position += button_logo_height + margin

        self.btn_income.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_outcome.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_wallet.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_history.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_statistic.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_category.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_wishlist.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.aboutUs.setGeometry(
            int((home_section_width - button_width) / 2),
            y_position,
            button_width,
            button_height
        )

        self.label.setGeometry(
            int((home_section_width - button_width) * 4), # Agar berada di bagian kanan
            y_position,
            button_width,
            button_height
        )

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.btn_income.setText(_translate("Form", " Edit Income"))
        self.btn_outcome.setText(_translate("Form", " Edit Outcome"))
        self.btn_wallet.setText(_translate("Form", " Wallet"))
        self.btn_history.setText(_translate("Form", " History"))
        self.btn_statistic.setText(_translate("Form", " Statistic"))
        self.btn_category.setText(_translate("Form", " Category"))
        self.btn_wishlist.setText(_translate("Form", " Wishlist"))
        self.label.setText(_translate("Form", "v1.2"))
