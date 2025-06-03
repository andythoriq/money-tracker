import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QSizePolicy, QPushButton
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5 import QtCore, QtGui
from utils.number_formatter import NumberFormat
from controller.wallet import Wallet

class SlidingWalletWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create stacked widget for sliding
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("stackedWidget")
        self.layout.addWidget(self.stacked_widget)

        # Populate wallet pages
        self.populate_wallet_pages()

        self.next_button = QPushButton(">")
        self.next_button.setObjectName("btn_nextslide")
        self.next_button.setGeometry(
            500,
            40,
            40,
            40
        )
        self.next_button.clicked.connect(lambda: (
            self.slide_next(),
            self.slide_timer.start(4000),  # Restart the timer after manual click
            self.refresh_wallets()
        ))
        self.layout.addWidget(self.next_button)

        # Setup sliding timer
        self.slide_timer = QTimer(self)
        self.slide_timer.timeout.connect(self.slide_next)
        self.slide_timer.start(4000)  # Slide every 4 seconds

        # Setup click event
        self.stacked_widget.mousePressEvent = self.on_click_slide

    def refresh_wallets(self):
        """
        Refreshes the wallet display by clearing current widgets and repopulating
        Call this method whenever a new wallet is added
        """
        # Remember current index to maintain position if possible
        current_index = self.stacked_widget.currentIndex()
        
        # Clear all widgets from stacked widget
        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        # Repopulate with fresh data
        self.populate_wallet_pages()
        
        # Restore index or set to 0 if new count is less than previous index
        if current_index >= 0 and current_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(current_index)
        elif self.stacked_widget.count() > 0:
            self.stacked_widget.setCurrentIndex(0)

    def populate_wallet_pages(self):
        # Get wallet names
        wallet_names = self.wallet_controller.get_wallet_name()

        if wallet_names:
            for name in wallet_names:
                # Get the balance for each wallet
                balance = self.wallet_controller.get_balance_by_name(name)
                
                # Create a page for each wallet
                page = QWidget()
                page.setObjectName("walletBox")
                page_layout = QVBoxLayout(page)
                page_layout.setContentsMargins(20, 20, 20, 20)
                
                wallet_label = QLabel(f"{name}")
                wallet_label.setObjectName("Label_1")
                
                balance_label = QLabel(f"Rp {NumberFormat.getFormattedMoney(balance):}")
                balance_label.setObjectName("Label_1")
                
                page_layout.addWidget(wallet_label)
                page_layout.addWidget(balance_label)
                page_layout.addStretch()
                
                self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.stacked_widget.setAttribute(Qt.WA_StyledBackground, True)
                self.stacked_widget.setObjectName("walletBox")
                self.stacked_widget.addWidget(page)
        else:
            # Create a "No Wallet" page
            no_wallet_page = QWidget()
            no_wallet_page.setObjectName("walletBox")
            no_wallet_layout = QVBoxLayout(no_wallet_page)
            no_wallet_layout.setContentsMargins(20, 20, 20, 20)
            
            no_wallet_label = QLabel("No Wallet")
            no_wallet_label.setObjectName("Label_1")
            no_wallet_layout.addWidget(no_wallet_label)
            no_wallet_layout.addStretch()
            
            self.stacked_widget.setAttribute(Qt.WA_StyledBackground, True)
            self.stacked_widget.addWidget(no_wallet_page)

    def slide_next(self):
        if self.stacked_widget.count() > 1:
            current_index = self.stacked_widget.currentIndex()
            next_index = (current_index + 1) % self.stacked_widget.count()
            self.slide_to_index(next_index)

    def on_click_slide(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.slide_next()

    def slide_to_index(self, next_index):
        current_widget = self.stacked_widget.currentWidget()
        next_widget = self.stacked_widget.widget(next_index)
        width = self.stacked_widget.width()

        # Current widget slides out to the left
        current_anim = QPropertyAnimation(current_widget, b"geometry")
        current_anim.setDuration(300)
        current_anim.setStartValue(current_widget.geometry())
        current_anim.setEndValue(QRect(-width, 0, width, current_widget.height()))
        current_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Next widget slides in from the right
        next_anim = QPropertyAnimation(next_widget, b"geometry")
        next_anim.setDuration(300)
        next_anim.setStartValue(QRect(width, 0, width, next_widget.height()))
        next_anim.setEndValue(QRect(0, 0, width, next_widget.height()))
        next_anim.setEasingCurve(QEasingCurve.OutCubic)

        # Start animations
        current_anim.start()
        next_anim.start()

        # Update the current index
        self.stacked_widget.setCurrentIndex(next_index)
