import json

class Outcome:
    FILE_PATH = "database/outcome.json"

    def __init__(self, wallet_controller):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)
        self.wallet_controller = wallet_controller

    def load_outcomes(self):
        """Memuat data outcome dari file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_outcomes(self, outcomes):
        """Menyimpan data outcome ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(outcomes, file, indent=4)

    def add_outcome(self, amount, category, wallet, desc, date):
        """Menambah outcome baru & update saldo wallet."""
        result = self.validate_outcome_data({
            "amount": amount,
            "category": category,
            "wallet": wallet,
            "desc": desc,
            "date": date
        }, False)
        if not result.get("valid"):
            return result  # Stop execution if validation fails

        outcomes = self.load_outcomes()
        outcomes.append({
            "ID": len(outcomes) + 1,
            "amount": amount,
            "category": category,
            "wallet": wallet,
            "desc": desc,
            "date": date
        })
        self.save_outcomes(outcomes)
        return result  # Return True if outcome is successfully added

    def update_outcome(self, updated_outcome):
        """Mengupdate data outcome."""
        outcomes = self.load_outcomes()
        for i, outcome in enumerate(outcomes):
            if outcome["ID"] == updated_outcome["ID"]:
                result = self.validate_outcome_data({
                    "amount": updated_outcome['amount'],
                    "category": updated_outcome['category'],
                    "wallet": updated_outcome['wallet'],
                    "desc": updated_outcome['desc'],
                    "date": updated_outcome['date']
                }, True)

                if not result.get("valid"):
                    return result # Stop execution if validation fails

                #update balance
                old_amount = int(outcome["amount"])
                new_amount = int(updated_outcome["amount"])
                self.wallet_controller.update_balance(outcome["wallet"], -old_amount, "Outcome")
                self.wallet_controller.update_balance(updated_outcome["wallet"], new_amount, "Outcome")
                
                outcomes[i] = updated_outcome
                self.save_outcomes(outcomes)
                return result  # Return True if outcome is successfully updated
        return False

    def delete_outcome(self, id):
        """Menghapus outcome dengan id."""
        outcomes = self.load_outcomes()
        deleted_outcome = next((outcome for outcome in outcomes if outcome["ID"] == id), None)
        if not deleted_outcome:
            return False
        self.wallet_controller.update_balance(deleted_outcome["wallet"], -int(deleted_outcome["amount"]), "Outcome")
        outcomes = [outcome for outcome in outcomes if outcome["ID"] != int(id)]
        self.save_outcomes(outcomes)
        return True
    
    def validate_outcome_data(self, outcome_data, is_edit):
        """
        Validate outcome data to ensure it meets the required criteria.
        :param outcome_data: Dictionary containing outcome data.
        :return: Dictionary with validation result and error messages.
        """
        required_fields = ['amount', 'category', 'wallet', 'desc', 'date']
        errors = {}
        
        for field in required_fields:
            if field not in outcome_data or not outcome_data[field]:
                errors[field] = f"tidak boleh kosong"

        if outcome_data.get('amount') > 9_999_999_999:
            errors["amount"] = "Jumlah saldo tidak boleh lebih dari 9.999.999.999."

        if not errors and not is_edit:
            wallet = outcome_data['wallet']
            amount = int(outcome_data['amount'])
            if not self.wallet_controller.update_balance(wallet, amount, "Outcome"):
                errors['wallet'] = "Gagal memperbarui saldo wallet"

        return {"valid": True} if not errors else {"valid": False, "errors": errors}