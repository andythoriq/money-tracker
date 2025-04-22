import json

class Income:
    FILE_PATH = "database/income.json"

    def __init__(self, wallet_controller):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)
        self.wallet_controller = wallet_controller

    def load_incomes(self):
        """Memuat data income dari file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_incomes(self, incomes):
        """Menyimpan data income ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(incomes, file, indent=4)

    def add_income(self, amount, category, wallet, desc, date):
        """Menambah income baru & update saldo wallet."""
        incomes = self.load_incomes()
        if self.wallet_controller.update_balance(wallet, int(amount), "income"):
            new_id = len(incomes) + 1
            incomes.append({
                "ID": new_id,
                "amount": amount,
                "category": category,
                "wallet": wallet,
                "desc": desc,
                "date": date
            })
            self.save_incomes(incomes)
            return True
        return False

    def update_income(self, updated_income):
        """Mengupdate data income."""
        incomes = self.load_incomes()
        for i, income in enumerate(incomes):
            if income["ID"] == updated_income["ID"]:
                old_amount = int(income["amount"])
                new_amount = int(updated_income["amount"])
                self.wallet_controller.update_balance(income["wallet"], -old_amount, "income")
                self.wallet_controller.update_balance(updated_income["wallet"], new_amount, "income")
                incomes[i] = updated_income
                break
        self.save_incomes(incomes)

    def delete_income(self, id):
        """Menghapus income dengan id."""
        incomes = self.load_incomes()
        deleted_income = next((income for income in incomes if income["ID"] == id), None)
        if not deleted_income:
            return False
        self.wallet_controller.update_balance(deleted_income["wallet"], -int(deleted_income["amount"]), "income")
        incomes = [income for income in incomes if income["ID"] != int(id)]
        self.save_incomes(incomes)
        return True
