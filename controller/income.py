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

    def update_income(self, updated_income):
        """Mengupdate data income"""
        incomes = self.load_incomes()
        for i, income in enumerate(incomes):
            if income[0] == updated_income[0]:  # ID
                # saldo
                old_amount = int(income[1])
                new_amount = int(updated_income[1])
                self.wallet_controller.update_balance(income[3], -old_amount, "income")  # Kurangi saldo lama
                self.wallet_controller.update_balance(updated_income[3], new_amount, "income")  # Tambah saldo baru
                
                # Iincome
                incomes[i] = updated_income
                break

        self.save_incomes(incomes)

    def delete_income(self, id):
        """Menghapus income dengan id"""
        incomes = self.load_incomes()

        deleted_income = [income for income in incomes if int(income[0]) == int(id)]
        
        if not deleted_income:
            return False

        deleted_income = deleted_income[0]

        self.wallet_controller.update_balance(deleted_income[3], -int(deleted_income[1]), "income")

        new_incomes = [income for income in incomes if int(income[0]) != int(id)]
        self.save_incomes(new_incomes)

        return True
