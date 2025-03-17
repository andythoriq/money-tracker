import os

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

    def add_wishlist(self, name, price, status):
        """Menambah wishlist baru"""
        self.wishlists.append([name, str(price), status])
        self.save_wishlists()