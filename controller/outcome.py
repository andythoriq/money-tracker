import os

class Outcome:
    FILE_PATH = "database/outcome.txt"

    def __init__(self, wallet_controller):
        self.wallet_controller = wallet_controller
        self.outcomes = self.load_outcomes()

    def load_outcomes(self):
        """Memuat data outcome dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_outcomes(self):
        """Menyimpan data outcome ke file"""
        with open(self.FILE_PATH, "w") as file:
            for outcome in self.outcomes:
                file.write(",".join(outcome) + "\n")

    def add_outcome(self, amount, category, wallet, description, date):
        """Menambah outcome baru & update saldo wallet"""
        new_id = str(len(self.outcomes) + 1)
        self.outcomes.append([new_id, str(amount), category, wallet, description, date])

        # Update saldo di wallet
        if (self.wallet_controller.update_balance(wallet, int(amount), "outcome")):
            self.save_outcomes()
            return True
        
        return False
