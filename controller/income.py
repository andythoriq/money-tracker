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

    def add_income(self, amount, category, wallet, desc, date):
        """Menambah income baru & update saldo wallet."""
        result = self.validate_income_data({
            "amount": amount,
            "category": category,
            "wallet": wallet,
            "desc": desc,
            "date": date
        }, False)
        if not result.get("valid"):
            return result  # Stop execution if validation fails

        incomes = self.load_incomes()
        incomes.append({
            "ID": len(incomes) + 1,
            "amount": amount,
            "category": category,
            "wallet": wallet,
            "desc": desc,
            "date": date
        })
        self.save_incomes(incomes)
        return result  # Return True if income is successfully added

    def update_income(self, updated_income):
        """Mengupdate data income"""
        incomes = self.load_incomes()
        for i, income in enumerate(incomes):
            if income["ID"] == updated_income["ID"]:
                result = self.validate_income_data({
                    "amount": updated_income['amount'],
                    "category": updated_income['category'],
                    "wallet": updated_income['wallet'],
                    "desc": updated_income['desc'],
                    "date": updated_income['date']
                }, True)

                if not result.get("valid"):
                    return result # Stop execution if validation fails

                old_amount = int(income["amount"])
                new_amount = int(updated_income["amount"])
                self.wallet_controller.update_balance(income["wallet"], -old_amount, "income")
                self.wallet_controller.update_balance(updated_income["wallet"], new_amount, "income")
                
                incomes[i] = updated_income
                self.save_incomes(incomes)
                return result  # Return True if income is successfully updated
        return False

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
    
    def validate_income_data(self, income_data, is_edit):
        """
        Validate income data to ensure it meets the required criteria.
        :param income_data: Dictionary containing income data.
        :return: Dictionary with validation result and error messages.
        """
        required_fields = ['amount', 'category', 'wallet', 'desc', 'date']
        errors = {}
        
        for field in required_fields:
            if field not in income_data or not income_data[field]:
                errors[field] = f"tidak boleh kosong"

        if income_data.get('amount') > 9_999_999_999:
            errors["amount"] = "Jumlah saldo tidak boleh lebih dari 9.999.999.999."

        if not errors and not is_edit:
            wallet = income_data['wallet']
            amount = int(income_data['amount'])
            if not self.wallet_controller.update_balance(wallet, amount, "income"):
                errors['wallet'] = "Gagal memperbarui saldo wallet"

        return {"valid": True} if not errors else {"valid": False, "errors": errors}
