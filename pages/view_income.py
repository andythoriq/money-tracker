from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from controller.income import Income

class IncomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.income_controller = Income()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Tambah Income")
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel("Masukkan Income:")
        self.input_income = QLineEdit(self)
        self.btn_submit = QPushButton("Simpan", self)
        self.btn_submit.clicked.connect(self.add_income)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_income)
        self.layout.addWidget(self.btn_submit)

        self.setLayout(self.layout)

    def add_income(self):
        amount = self.input_income.text()
        if amount:
            self.income_controller.add_income(amount, "Gaji", "Dompet", "Pemasukan bulanan", "2025-02-28")
            self.close()