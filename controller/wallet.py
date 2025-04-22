import json

class Wallet:
    FILE_PATH = "database/wallet.json"

    def __init__(self):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)

    def load_wallets(self):
        """Memuat data wallet dari file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_wallets(self, wallets):
        """Menyimpan data wallet ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(wallets, file, indent=4)

    def add_wallet(self, name, amount):
        """Menambah wallet baru."""
        wallets = self.load_wallets()
        wallets.append({"name": name, "amount": amount})
        self.save_wallets(wallets)

    def edit_wallet(self, name, new_amount):
        """Mengedit saldo wallet."""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet["name"] == name:
                wallet["amount"] = new_amount
                self.save_wallets(wallets)
                return True
        return False

    def delete_wallet(self, name):
        """Menghapus wallet."""
        wallets = self.load_wallets()
        wallets = [wallet for wallet in wallets if wallet["name"] != name]
        self.save_wallets(wallets)

    def update_balance(self, name, amount, transaction_type):
        """Mengupdate saldo wallet berdasarkan transaksi."""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet["name"] == name:
                current_balance = wallet["amount"]
                if transaction_type == "income":
                    wallet["amount"] = current_balance + amount
                elif transaction_type == "outcome":
                    if current_balance < amount:
                        return False
                    wallet["amount"] = current_balance - amount
                self.save_wallets(wallets)
                return True
        return False

    def get_wallet_by_name(self, name):
        """Mendapatkan informasi wallet berdasarkan nama."""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet["name"] == name:
                return wallet
        return None

    def get_balance_by_name(self, name):
        """Mendapatkan saldo wallet berdasarkan nama."""
        wallet = self.get_wallet_by_name(name)
        return wallet["amount"] if wallet else None
    
    def get_wallet_name(self):
        wallets = self.load_wallets()
        name = [line.get('name') for line in wallets]  # Ambil hanya nama wallet
        return name