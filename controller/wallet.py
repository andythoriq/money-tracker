import os

class Wallet:
    FILE_PATH = "database/wallet.txt"

    def __init__(self):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w"):
                pass

    def load_wallets(self):
        """Memuat data wallet dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
        
    def load_wallet_names(self):
        """Memuat nama wallet dari file"""
        wallets = self.load_wallets()
        return [wallet[0] for wallet in wallets if len(wallet) > 0]

    def save_wallets(self, wallets):
        """Menyimpan data wallet ke file"""
        with open(self.FILE_PATH, "w") as file:
            for wallet in wallets:
                file.write(",".join(wallet) + "\n")

    def add_wallet(self, name, amount):
        """Menambah wallet baru"""
        wallets = self.load_wallets()
        wallets.append([name, str(amount)])
        self.save_wallets(wallets)

    def edit_wallet(self, name, new_amount):
        """Mengedit saldo wallet"""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet[0] == name:
                wallet[1] = str(new_amount)
                self.save_wallets(wallets)
                return True
        return False

    def delete_wallet(self, name):
        """Menghapus wallet"""
        wallets = self.load_wallets()
        wallets = [wallet for wallet in wallets if wallet[0] != name]
        self.save_wallets(wallets)

    def update_balance(self, name, amount, transaction_type):
        """Mengupdate saldo wallet berdasarkan transaksi"""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet[0] == name:
                current_balance = int(wallet[1])
                if transaction_type == "income":
                    wallet[1] = str(current_balance + amount)
                elif transaction_type == "outcome":
                    if current_balance < amount:
                        return False
                    wallet[1] = str(current_balance - amount)

                self.save_wallets(wallets)
                return True
        return False
