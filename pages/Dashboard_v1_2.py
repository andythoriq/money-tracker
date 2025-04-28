import os
from PyQt5.QtGui import QFont, QFontMetrics # untuk mengubah font agar sesuai dengan size dari layout font tersebut
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget, QGroupBox, QHBoxLayout
from PyQt5 import QtGui, QtCore, QtWidgets
from pages.view_wallet import WalletView
from pages.view_income import IncomeView
from pages.view_outcome import OutcomeView
from pages.view_history import HistoryView
from pages.view_category import CategoryView
from pages.view_wishlist import WishlistView
from pages.view_login import LoginScreen
from pages.view_register import RegisterScreen
from controller.Popup import PopupAboutUs
from controller.wallet import Wallet
from controller.Sliding import SlidingWalletWidget

class Dashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()
        self.resize(1366, 768)  # Ukuran awal jendela

    def init_ui(self):
        """Inisialisasi tampilan UI utama"""
        self.setWindowTitle("Money Tracker")

        self.wallet_controller = Wallet()

        # Stack untuk menyimpan berbagai halaman
        self.stack = QStackedWidget()

        self.container = QGroupBox()
        self.container.setObjectName("container")
        self.container.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.container.setMinimumSize(0, 0)

        # Sidebar kiri (HomeSection)
        self.HomeSection = QGroupBox()

        # Inisialisasi view-view lainnya
        self.wallet_view = WalletView(self.stack)
        self.income_view = IncomeView(self.stack)
        self.outcome_view = OutcomeView(self.stack)
        self.history_view = HistoryView(self.stack)
        self.category_view = CategoryView(self.stack)
        self.wishlist_view = WishlistView(self.stack)

        # Menambahkan halaman ke stack
        self.stack.addWidget(self.container)
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
        main_layout.addWidget(self.HomeSection, 10) # Sidebar kiri (22%)
        main_layout.addWidget(self.stack, 36) # Konten utama (78%)
        self.setLayout(main_layout)
        
    def init_main_menu(self):
        """Inisialisasi tampilan sidebar dan konten utama"""

        self.HomeSection.setObjectName("HomeSection")
        self.HomeSection.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.HomeSection.setMinimumSize(296, 768)
    
        self.layout_1 = QGroupBox(self.container)
        self.layout_1.setObjectName("Layout")
        self.layout_1_ui()

        self.layout_2 = QGroupBox(self.container)
        self.layout_2.setObjectName("Layout")
        self.layout_3 = QGroupBox(self.container)
        self.layout_3.setObjectName("Layout")
        self.layout_4 = QGroupBox(self.container)
        self.layout_4.setObjectName("Layout")

        # Tombol-tombol Sidebar (HomeSection)
        self.btn_home = QPushButton(self.HomeSection)
        self.btn_home.setIcon(QtGui.QIcon("../money-tracker/img/icon/logo-app.png"))
        self.btn_home.setIconSize(QtCore.QSize(80, 80))
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentWidget(self.container))
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

    def layout_1_ui(self):

        # Create the sliding wallet widget
        self.sliding_wallet_widget = SlidingWalletWidget(self.container)

        # Create a layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.sliding_wallet_widget)
        
        # Set the layout for layout_1
        self.layout_1.setLayout(layout)

    def layout_2_ui(self):
        layout = QVBoxLayout()

        self.layout_2.setLayout(layout)

    def resizeEvent(self, event):
        """Override resizeEvent untuk menyesuaikan ukuran dan posisi tombol"""
        super().resizeEvent(event)
        self.update_button_geometry()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_button_geometry()  # container sudah dihitung ukurannya

    def update_button_geometry(self):
        """Menghitung ulang posisi dan ukuran tombol berdasarkan ukuran jendela"""
        # Dapatkan ukuran HomeSection
        home_section_width = self.HomeSection.width()
        home_section_height = self.HomeSection.height()
        container_section_width = self.container.width()
        container_section_height = self.container.height()

        # Atur ukuran dan posisi tombol
        button_width = int(home_section_width / 1.15)  # Lebar tombol sesuai dengan lebar layout dari homesection
        button_height = int(home_section_height / 12)  # Tinggi tombol sesuai dengan tinggi layout dari homesection
        button_logo_height = int(home_section_height / 6) # Khusus untuk tombol logo app
        margin = int(home_section_width * 0.0348)  # Jarak antar tombol
        
        # Atur ukuran dan posisi layout
        button_layout1_width = int(container_section_width * (425/1070))
        button_layout1_height = int(container_section_height * (186/768))
        button_layout2_width = int(container_section_width * (425/1070))
        button_layout2_height = int(container_section_height * (479/768))
        button_layout3_width = int(container_section_width * (544/1070))
        button_layout3_height = int(container_section_height * (428/768))
        button_layout4_width = int(container_section_width * (544/1070))
        button_layout4_height = int(container_section_height * (238/768))

        # Posisi awal tombol
        x_position =  int((home_section_width - button_width) / 2)
        y_position = 23
        aboutus_x_position = int((home_section_width - button_width) / 2)
        x_position_layout = int(container_section_width * (32/1070))
        y_position_layout = int(container_section_height * (43/768))

        # Ukuran dari ikon tombol
        icon_width = int(home_section_width / 6)
        icon_height = int((home_section_height / 10) - 20)
        icon_app_width = int(home_section_width / 4)
        icon_app_height = int(home_section_height / 4)

        # Atur ukuran ikon tombol agar sesuai dengan layout tombol tersebut
        self.btn_home.setIconSize(QtCore.QSize(
            icon_app_width, 
            icon_app_height
        ))

        self.btn_income.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        self.btn_outcome.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        self.btn_wallet.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        self.btn_history.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        self.btn_statistic.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        self.btn_category.setIconSize(QtCore.QSize(
            icon_width, 
            icon_height
        ))

        self.btn_wishlist.setIconSize(QtCore.QSize(
            icon_width,
            icon_height
        ))

        # Atur font agar sesuai dengan size dari layout font tersebut
        font_size = int(home_section_height / 10)

        # Atur ulang posisi dan ukuran tombol
        self.btn_home.setGeometry(
            x_position,  # Tengah horizontal
            y_position,
            button_width,
            button_logo_height
        )
        y_position += button_logo_height + margin

        self.btn_income.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_outcome.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_wallet.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_history.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_statistic.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_category.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin

        self.btn_wishlist.setGeometry(
            x_position,
            y_position,
            button_width,
            button_height
        )
        y_position += button_height + margin + 20

        self.aboutUs.setGeometry(
            aboutus_x_position,
            y_position,
            button_width,
            button_height
        )

        self.label.setGeometry(
            int(aboutus_x_position * 11), # Agar berada di bagian kanan
            y_position,
            button_width,
            button_height
        )

        margin = 22
        
        self.layout_1.setGeometry(
            x_position_layout,
            y_position_layout,
            button_layout1_width,
            button_layout1_height
        )
        y_position_layout_2 = y_position_layout + button_layout1_height + margin

        self.layout_2.setGeometry(
            x_position_layout,
            y_position_layout_2,
            button_layout2_width,
            button_layout2_height
        )

        x_position_layout += int(button_layout1_width + margin)

        self.layout_3.setGeometry(
            x_position_layout,
            y_position_layout,
            button_layout3_width,
            button_layout3_height
        )
        y_position_layout += int(button_layout3_height + margin)

        self.layout_4.setGeometry(
            x_position_layout,
            y_position_layout,
            button_layout4_width,
            button_layout4_height
        )

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Money Tracker"))
        self.btn_income.setText(_translate("Form", " Edit Income"))
        self.btn_outcome.setText(_translate("Form", " Edit Outcome"))
        self.btn_wallet.setText(_translate("Form", " Wallet"))
        self.btn_history.setText(_translate("Form", " History"))
        self.btn_statistic.setText(_translate("Form", " Statistic"))
        self.btn_category.setText(_translate("Form", " Category"))
        self.btn_wishlist.setText(_translate("Form", " Wishlist"))
        self.label.setText(_translate("Form", "v1.2"))