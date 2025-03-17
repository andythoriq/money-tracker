import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

class Wishlist:
    FILE_PATH = "database/wishlist.txt"

    def __init__(self):
        self.wishlists = self.load_wishlists()

    def load_wishlists(self):
        """Memuat data wishlist dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_wishlists(self):
        """Menyimpan data wishlist ke file"""
        with open(self.FILE_PATH, "w") as file:
            for wishlist in self.wishlists:
                file.write(",".join(wishlist) + "\n")

    def add_wishlist(self, name, price):
        """Menambah wishlist baru"""
        self.wishlists.append([name, str(price)])
        self.save_wishlists()

    def delete_wishlist(self, index):
        """Menghapus wishlist berdasarkan index"""
        if 0 <= index < len(self.wishlists):
            self.wishlists.pop(index)
            self.save_wishlists()

class WishlistView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.wishlist = Wishlist()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Nama Wishlist')
        self.name_input.returnPressed.connect(self.save_wishlist)  # Simpan saat tekan Enter
        layout.addWidget(self.name_input)

        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText('Harga')
        self.price_input.returnPressed.connect(self.save_wishlist)  # Simpan saat tekan Enter
        layout.addWidget(self.price_input)

        # Wishlist display
        self.wishlist_display = QListWidget(self)
        self.wishlist_display.keyPressEvent = self.handle_key_press  # Tangani tombol keyboard
        layout.addWidget(self.wishlist_display)

        # Load existing wishlists
        self.load_wishlists()

        self.setLayout(layout)

    def load_wishlists(self):
        """Memuat wishlist ke dalam QListWidget"""
        self.wishlist_display.clear()
        for item in self.wishlist.wishlists:
            self.wishlist_display.addItem(f"{item[0]} - {item[1]}")

    def save_wishlist(self):
        """Menyimpan wishlist secara otomatis"""
        name = self.name_input.text()
        price = self.price_input.text()

        if name and price:
            self.wishlist.add_wishlist(name, price)
            self.load_wishlists()
            self.name_input.clear()
            self.price_input.clear()
        else:
            QMessageBox.warning(self, 'Input Error', 'Nama dan harga harus diisi!')

    def handle_key_press(self, event):
        """Menangani tombol keyboard untuk menghapus wishlist"""
        if event.key() == Qt.Key_Delete:  # Jika tombol Delete ditekan
            selected_item = self.wishlist_display.currentRow()
            if selected_item >= 0:
                self.wishlist.delete_wishlist(selected_item)
                self.load_wishlists()
            else:
                QMessageBox.warning(self, 'Peringatan', 'Pilih wishlist yang ingin dihapus!')
        else:
            super().keyPressEvent(event)  # Tetap jalankan event default