import os

class Wallet:
    FILE_PATH = "database/wallet.txt"

    def __init__(self):
        self.wallets = self.load_wallets()

    def load_wallets(self):
        """Memuat data wallet dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_wallets(self):
        """Menyimpan data wallet ke file"""
        with open(self.FILE_PATH, "w") as file:
            for wallet in self.wallets:
                file.write(",".join(wallet) + "\n")

    def add_wallet(self, name, amount):
        """Menambah wallet baru"""
        self.wallets.append([name, str(amount)])
        self.save_wallets()

    def edit_wallet(self, name, new_amount):
        """Mengedit saldo wallet"""
        for wallet in self.wallets:
            if wallet[0] == name:
                wallet[1] = str(new_amount)
                self.save_wallets()
                return True
        return False

    def delete_wallet(self, name):
        """Menghapus wallet"""
        self.wallets = [wallet for wallet in self.wallets if wallet[0] != name]
        self.save_wallets()

    def update_balance(self, name, amount, transaction_type):
        """Mengupdate saldo wallet berdasarkan transaksi"""
        for wallet in self.wallets:
            if wallet[0] == name:
                current_balance = int(wallet[1])
                if transaction_type == "income":
                    wallet[1] = str(current_balance + amount)
                elif transaction_type == "outcome":
                    if (current_balance < int(amount)):
                        return False

                    wallet[1] = str(current_balance - amount)

                self.save_wallets()
                return True

        return False
