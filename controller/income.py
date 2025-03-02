import os

class Income:
    FILE_PATH = "database/income.txt"

    def __init__(self, wallet_controller):
        self.wallet_controller = wallet_controller
        self.incomes = self.load_incomes()

    def load_incomes(self):
        """Memuat data income dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_incomes(self):
        """Menyimpan data income ke file"""
        with open(self.FILE_PATH, "w") as file:
            for income in self.incomes:
                file.write(",".join(income) + "\n")

    def add_income(self, amount, category, wallet, description, date):
        """Menambah income baru & update saldo wallet"""
        new_id = str(len(self.incomes) + 1)
        self.incomes.append([new_id, str(amount), category, wallet, description, date])

        # Update saldo di wallet
        if (self.wallet_controller.update_balance(wallet, int(amount), "income")):
            self.save_incomes()
            return True
        
        return False
