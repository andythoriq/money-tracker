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

    def update_outcome(self, updated_outcome):
        """Mengupdate data outcome"""
        outcomes = self.load_outcomes()
        for i, outcome in enumerate(outcomes):
            if outcome[0] == updated_outcome[0]:  # ID
                # Update saldo
                old_amount = int(outcome[1])
                new_amount = int(updated_outcome[1])
                self.wallet_controller.update_balance(outcome[3], -old_amount, "outcome")  # Tambah saldo lama
                self.wallet_controller.update_balance(updated_outcome[3], new_amount, "outcome")  # Kurangi saldo baru
                
                # Outcome
                outcomes[i] = updated_outcome
                break

        self.save_outcomes(outcomes)  # Simpan ke file

    def delete_outcome(self, id):
        """Menghapus outcome dengan id"""
        outcomes = self.load_outcomes()

        deleted_outcome = [outcome for outcome in outcomes if int(outcome[0]) == int(id)]
        
        if not deleted_outcome:
            return False

        deleted_outcome = deleted_outcome[0]

        self.wallet_controller.update_balance(deleted_outcome[3], -int(deleted_outcome[1]), "outcome")

        new_outcomes = [outcome for outcome in outcomes if int(outcome[0]) != int(id)]
        self.save_outcomes(new_outcomes)

        return True
