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
        outcomes = self.load_outcomes()
        if self.wallet_controller.update_balance(wallet, int(amount), "outcome"):
            new_id = len(outcomes) + 1
            outcomes.append({
                "ID": new_id,
                "amount": amount,
                "category": category,
                "wallet": wallet,
                "desc": desc,
                "date": date
            })
            self.save_outcomes(outcomes)
            return True
        return False

    def update_outcome(self, updated_outcome):
        """Mengupdate data outcome."""
        outcomes = self.load_outcomes()
        for i, outcome in enumerate(outcomes):
            if outcome["ID"] == updated_outcome["ID"]:
                old_amount = int(outcome["amount"])
                new_amount = int(updated_outcome["amount"])
                self.wallet_controller.update_balance(outcome["wallet"], -old_amount, "outcome")
                self.wallet_controller.update_balance(updated_outcome["wallet"], new_amount, "outcome")
                outcomes[i] = updated_outcome
                break
        self.save_outcomes(outcomes)

    def delete_outcome(self, id):
        """Menghapus outcome dengan id."""
        outcomes = self.load_outcomes()
        deleted_outcome = next((outcome for outcome in outcomes if outcome["ID"] == id), None)
        if not deleted_outcome:
            return False
        self.wallet_controller.update_balance(deleted_outcome["wallet"], -int(deleted_outcome["amount"]), "outcome")
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
            if not self.wallet_controller.update_balance(wallet, amount, "outcome"):
                errors['wallet'] = "Gagal memperbarui saldo wallet"

        return {"valid": True} if not errors else {"valid": False, "errors": errors}