import os

class Income:
    FILE_PATH = "database/income.txt"

    def __init__(self, wallet_controller):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w"):
                pass
        
        self.wallet_controller = wallet_controller

    def load_incomes(self):
        """Memuat data income dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_incomes(self, incomes):
        """Menyimpan data income ke file"""
        with open(self.FILE_PATH, "w") as file:
            for income in incomes:
                file.write(",".join(income) + "\n")

    def add_income(self, amount, category, wallet, description, date):
        """Menambah income baru & update saldo wallet"""
        incomes = self.load_incomes()
        
        # Update saldo di wallet
        if self.wallet_controller.update_balance(wallet, int(amount), "income"):
            new_id = str(len(incomes) + 1)
            incomes.append([new_id, str(amount), category, wallet, description, date])
            self.save_incomes(incomes)
            return True
        
        return False
