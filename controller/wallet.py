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

        # validasi
        result = self.validate_wallet_data({'name': name, 'amount': amount}, is_edit=False)
        if not result.get("valid"):
            return result

        wallets.append({"name": name, "amount": amount})
        self.save_wallets(wallets)
        return result

    def edit_wallet(self, name, new_amount):
        """Mengedit saldo wallet"""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet["name"] == name:

                # validasi
                result = self.validate_wallet_data({'name': name, 'amount': new_amount}, is_edit=True)
                if not result.get("valid"):
                    return result # Stop execution if validation fails

                wallet["amount"] = new_amount
                self.save_wallets(wallets)
                return result  
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

    def get_wallet_by_name(self, name):
        """Mendapatkan informasi wallet berdasarkan nama"""
        wallets = self.load_wallets()
        for wallet in wallets:
            if wallet[0] == name:
                return wallet  # Mengembalikan data wallet dalam bentuk [name, balance]
        return None  # Jika tidak ditemukan

    def get_balance_by_name(self, name):
        """Mendapatkan saldo wallet berdasarkan nama"""
        wallet = self.get_wallet_by_name(name)
        return int(wallet[1]) if wallet else None  # Mengembalikan saldo atau None jika tidak ditemukan
    
    def get_wallet_name(self):
        wallets = self.load_wallets()
        name = [line[0] for line in wallets]  # Ambil hanya nama wallet
        return name
    
    def validate_wallet_data(self, wallet_data, is_edit):
        """
        Validate wallet data to ensure it meets the required criteria.
        :param wallet_data: Dictionary containing wallet data.
        :return: Dictionary with validation result and error messages.
        """
        errors = {}
        
        if not isinstance(wallet_data.get('amount'), (int, float)) or wallet_data.get('amount') < 0:
            errors["amount"] = "Jumlah saldo harus berupa angka positif."

        if wallet_data.get('amount') > 9_999_999_999:
            errors["amount"] = "Jumlah saldo tidak boleh lebih dari 9.999.999.999."

        if not is_edit:
            if not wallet_data.get('name'):
                errors["name"] = "wallet tidak boleh kosong."
            elif wallet_data.get('name') in self.get_wallet_name():
                errors["name"] = "wallet sudah ada."
            elif len(wallet_data.get('name')) < 3:
                errors["name"] = "wallet harus lebih dari 3 karakter."
            elif len(wallet_data.get('name')) > 20:
                errors["name"] = "wallet tidak boleh lebih dari 20 karakter."
            elif not wallet_data.get('name').isalnum():
                errors["name"] = "wallet hanya boleh mengandung huruf dan angka."
            elif not wallet_data.get('name')[0].isalpha():
                errors["name"] = "wallet harus diawali dengan huruf."

        return {"valid": not bool(errors), "errors": errors}