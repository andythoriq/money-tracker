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
from controller.wallet import Wallet

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

        self.wallet_controller = Wallet()

        # Stack untuk menyimpan berbagai halaman
        self.stack = QStackedWidget()

        # Halaman utama (Dashboard)
        self.main_menu = QWidget()
        self.main_menu.setObjectName("main_menu")

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
        self.container = QGroupBox(self.main_menu)
        self.container.setObjectName("container")
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        self.layout_1 = QGroupBox(self.container)
        self.layout_1.setObjectName("Layout")
        self.layout_1_ui()

        self.layout_2 = QGroupBox(self.container)
        self.layout_2.setObjectName("Layout")
        self.layout_3 = QGroupBox(self.container)
        self.layout_3.setObjectName("Layout")
        self.layout_4 = QGroupBox(self.container)
        self.layout_4.setObjectName("Layout")

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
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_menu))

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

    def layout_1_ui(self):
        layout = QVBoxLayout()
        self.wallet_name = self.wallet_controller.get_wallet_name()
        self.wallet_balance = self.wallet_controller.get_balance_by_name(self.wallet_name[0])
        self.wallet_label = QLabel(self.wallet_name[0])
        self.wallet_label.setObjectName("Label_1")
        self.balance_label = QLabel(f"Rp. {str(self.wallet_balance)}")
        self.balance_label.setObjectName("Label_1")

        layout.addWidget(self.wallet_label)
        layout.addWidget(self.balance_label)

        self.layout_1.setLayout(layout)

    def layout_2_ui(self):
        layout = QVBoxLayout()

        self.layout_2.setLayout(layout)



    def switch_page(self, page):
        if page == "dashboard":
            self.stack.setCurrentWidget(self.main_menu)
            self.container.setVisible(True)  # Tampilkan Container
        else:
            self.stack.setCurrentWidget(page)
            self.container.setVisible(False)  # Sembunyikan Container


    def resizeEvent(self, event):
        """Override resizeEvent untuk menyesuaikan ukuran dan posisi tombol"""
        super().resizeEvent(event)
        self.update_button_geometry()

    def update_button_geometry(self):
        """Menghitung ulang posisi dan ukuran tombol berdasarkan ukuran jendela"""
        # Dapatkan ukuran HomeSection
        home_section_width = self.HomeSection.width()
        home_section_height = self.HomeSection.height()

        container_section_width = self.container.width()
        container_section_height = self.container.height()
        button_layout_width = int(498)
        button_layout_height = int(218)

        # Atur ukuran dan posisi tombol
        button_width = int(290)
        button_height = int(76)
        button_logo_height = int(150) # Khusus untuk tombol logo app
        margin = 12  # Jarak antar tombol

        # Posisi awal tombol
        y_position = 10
        x_position = 30

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
        y_position = 40
        margin = 22
        
        self.layout_1.setGeometry(
            x_position,
            y_position,
            button_layout_width,
            button_layout_height
        )
        y_position += button_layout_height + margin
        button_layout_height += 343

        self.layout_2.setGeometry(
            x_position,
            y_position,
            button_layout_width,
            button_layout_height
        )
        y_position = 40
        x_position += int(button_layout_width + margin)
        button_layout_width = 638
        button_layout_height = 502

        self.layout_3.setGeometry(
            x_position,
            y_position,
            button_layout_width,
            button_layout_height
        )
        y_position += int(button_layout_height + margin)
        button_layout_height -= 222

        self.layout_4.setGeometry(
            x_position,
            y_position,
            button_layout_width,
            button_layout_height
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
