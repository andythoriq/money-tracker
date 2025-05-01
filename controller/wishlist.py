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

    def add_wishlist(self, label, price, status):
        """Menambah wishlist baru dengan ID."""

        # validasi
        result = self.validate_wishlist({
            "label": label,
            "price": price,
            "status": status
        })

        if not result.get("valid"):
            return result

        self.wishlists.append({
            "ID": len(self.wishlists) + 1,
            "label": label,
            "price": price,
            "status": status
        })
        self.save_wishlists()
        return result

    def edit_wishlist(self, wishlist_id, label, price, status):
        """Mengedit wishlist berdasarkan ID."""
        for wishlist in self.wishlists:
            if wishlist["ID"] == wishlist_id:
                result = self.validate_wishlist({
                    "label": label,
                    "price": price,
                    "status": status
                })
                if not result.get("valid"):
                    return result # Stop execution if validation fails

                wishlist["label"] = label
                wishlist["price"] = price
                wishlist["status"] = status

                self.save_wishlists()
                return result
        return False

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
        return [wishlist for wishlist in self.wishlists if wishlist["price"] <= saldo_wallet]

    def validate_wishlist(self, wishlist_data):
        required_fields = ['label', 'price']
        errors = {}
        
        for field in required_fields:
            if field not in wishlist_data or not wishlist_data[field]:
                errors[field] = f"tidak boleh kosong"

        if not errors:
            if wishlist_data.get('price') < 0:
                errors["price"] = "Jumlah saldo tidak boleh kurang dari 0."
            elif wishlist_data.get('price') > 9_999_999_999:
                errors["price"] = "Jumlah saldo tidak boleh lebih dari 9.999.999.999."

            if not wishlist_data.get('label'):
                errors["label"] = "tidak boleh kosong."
            elif len(wishlist_data.get('label')) < 3:
                errors["label"] = "harus lebih dari 3 karakter."
            elif len(wishlist_data.get('label')) > 64:
                errors["label"] = "tidak boleh lebih dari 20 karakter."
            elif not wishlist_data.get('label').isalnum():
                errors["label"] = "hanya boleh mengandung huruf dan angka."
            elif not wishlist_data.get('label')[0].isalpha():
                errors["label"] = "harus diawali dengan huruf."
        
        return {"valid": True} if not errors else {"valid": False, "errors": errors}