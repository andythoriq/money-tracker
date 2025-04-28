import os

class Wishlist:
    FILE_PATH = "database/wishlist.txt"

    def __init__(self, wallet_controller):
        self.wishlists = self.load_wishlists()
        self.wallet_controller = wallet_controller

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
        """Menambah wishlist baru dengan ID"""
        new_id = str(len(self.wishlists) + 1)
        self.wishlists.append([new_id, name, str(price), str(status).lower()])  
        self.save_wishlists()
        return new_id

    def edit_wishlist(self, wishlist_id, name, price, status):
        """Mengedit wishlist berdasarkan ID"""
        updated = False
        for wishlist in self.wishlists:
            if wishlist[0] == str(wishlist_id):
                wishlist[1] = name
                wishlist[2] = str(price)
                wishlist[3] = str(status).lower()
                updated = True
                break

        if updated:
            self.save_wishlists()
        return updated

    def delete_wishlist(self, wishlist_id):
        """Menghapus wishlist berdasarkan ID"""
        new_wishlists = [wishlist for wishlist in self.wishlists if wishlist[0] != str(wishlist_id)]

        if len(new_wishlists) != len(self.wishlists):
            self.wishlists = new_wishlists
            self.save_wishlists()
            return True
        
        return False

    def filter_wishlists(self, status_filter):
        """Menampilkan wishlist berdasarkan status (True/False)"""
        return [wishlist for wishlist in self.wishlists if wishlist[3] == str(status_filter).lower()]
    
    def filter_by_wallet(self, nama_wallet):
        """Menampilkan wishlist yang bisa dibeli dengan saldo wallet tertentu"""
        saldo_wallet = self.wallet_controller.get_balance_by_name(nama_wallet)
        if saldo_wallet is None:
            return []
        
        return [wishlist for wishlist in self.wishlists if int(wishlist[2]) <= saldo_wallet]
