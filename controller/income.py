import os

class Income:
    FILE_PATH = "database/income.txt"

    def __init__(self):
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
        """Menambah pemasukan baru"""
        self.incomes.append([str(amount), category, wallet, description, date])
        self.save_incomes()