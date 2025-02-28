import os

class Outcome:
    FILE_PATH = "database/outcome.txt"

    def __init__(self):
        self.outcomes = self.load_outcomes()

    def load_outcomes(self):

        if not os.path.exists(self.FILE_PATH):
            return []
        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_outcomes(self):

        with open(self.FILE_PATH, "w") as file:
            for outcome in self.outcomes:
                file.write(",".join(outcome) + "\n")

    def add_outcome(self, amount, category, wallet, description, date):
        """Menambah pengeluaran baru"""
        self.outcomes.append([str(amount), category, wallet, description, date])
        self.save_outcomes()