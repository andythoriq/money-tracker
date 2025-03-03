import os

class Outcome:
    FILE_PATH = "database/outcome.txt"

    def __init__(self, wallet_controller):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w"):
                pass
        
        self.wallet_controller = wallet_controller

    def load_outcomes(self):
        """Memuat data outcome dari file"""
        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_outcomes(self, outcomes):
        """Menyimpan data outcome ke file"""
        with open(self.FILE_PATH, "w") as file:
            for outcome in outcomes:
                file.write(",".join(outcome) + "\n")

    def add_outcome(self, amount, category, wallet, description, date):
        """Menambah outcome baru & update saldo wallet"""
        outcomes = self.load_outcomes()  # Memuat data terbaru dari file
        
        # Update saldo di wallet
        if self.wallet_controller.update_balance(wallet, int(amount), "outcome"):
            new_id = str(len(outcomes) + 1)
            outcomes.append([new_id, str(amount), category, wallet, description, date])
            self.save_outcomes(outcomes)
            return True
        
        return False
