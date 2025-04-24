import json

class Wishlist:
    FILE_PATH = "database/wishlist.json"

    def __init__(self, wallet_controller):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)
        self.wishlists = self.load_wishlists()
        self.wallet_controller = wallet_controller

    def load_wishlists(self):
        """Memuat data wishlist dari file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_wishlists(self):
        """Menyimpan data wishlist ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(self.wishlists, file, indent=4)

    def add_wishlist(self, label, price, status):
        """Menambah wishlist baru dengan ID."""
        new_id = str(len(self.wishlists) + 1)
        self.wishlists.append({
            "ID": new_id,
            "label": label,
            "price": price,
            "status": status
        })
        self.save_wishlists()
        return new_id

    def edit_wishlist(self, wishlist_id, label, price, status):
        """Mengedit wishlist berdasarkan ID."""
        updated = False
        for wishlist in self.wishlists:
            if wishlist["ID"] == wishlist_id:
                wishlist["label"] = label
                wishlist["price"] = price
                wishlist["status"] = status
                updated = True
                break
        if updated:
            self.save_wishlists()
        return updated

    def delete_wishlist(self, wishlist_id):
        """Menghapus wishlist berdasarkan ID."""
        new_wishlists = [wishlist for wishlist in self.wishlists if wishlist["ID"] != int(wishlist_id)]
        if len(new_wishlists) != len(self.wishlists):
            self.wishlists = new_wishlists
            self.save_wishlists()
            return True
        return False

    def filter_wishlists(self, status_filter):
        """Menampilkan wishlist berdasarkan status."""
        return [wishlist for wishlist in self.wishlists if wishlist["status"] == status_filter]

    def filter_by_wallet(self, nama_wallet):
        """Menampilkan wishlist yang bisa dibeli dengan saldo wallet tertentu."""
        saldo_wallet = self.wallet_controller.get_balance_by_name(nama_wallet)
        if saldo_wallet is None:
            return []
        return [wishlist for wishlist in self.wishlists if wishlist["price"] <= saldo_wallet]
