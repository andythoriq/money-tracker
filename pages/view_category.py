from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from controller.category import Category

class CategoryView(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.category_controller = Category()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Manage Categories")

        layout = QVBoxLayout()

        # === FORM INPUT ===
        form_layout = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Category Name")

        self.input_type = QComboBox()
        self.input_type.addItems(["income", "outcome"])  # Pilihan kategori

        self.btn_add = QPushButton("Add Category")
        self.btn_add.clicked.connect(self.add_category)

        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_type)
        form_layout.addWidget(self.btn_add)

        layout.addLayout(form_layout)

        # === TABEL KATEGORI ===
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "D"])
        layout.addWidget(self.table)

        # === TOMBOL BACK ===
        self.btn_back = QPushButton("Back to Dashboard")
        self.btn_back.clicked.connect(self.back_to_dashboard)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

        self.load_categories()

    def add_category(self):
        """Menambahkan kategori baru"""
        name = self.input_name.text().strip()
        category_type = self.input_type.currentText()

        if not name:
            QMessageBox.warning(self, "Warning", "Category name cannot be empty!")
            return

        self.category_controller.add_category(name, category_type)
        self.input_name.clear()
        self.load_categories()

    def load_categories(self):
        """Memuat ulang data kategori ke tabel"""
        self.table.setRowCount(0)
        categories = self.category_controller.load_categories()

        for row_idx, (name, category_type) in enumerate(categories):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(category_type))

            # Tombol Delete
            btn_delete = QPushButton("Delete")
            btn_delete.clicked.connect(lambda _, n=name, t=category_type: self.confirm_delete(n,t))
            self.table.setCellWidget(row_idx, 2, btn_delete)

    def confirm_delete(self, name, category_type):
        """Popup konfirmasi sebelum menghapus kategori"""
        reply = QMessageBox.question(
            self, "Delete Category",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.category_controller.delete_category(name, category_type)
            self.load_categories()

    def back_to_dashboard(self):
        """Kembali ke Dashboard"""
        self.stack.setCurrentIndex(0)  # Asumsikan dashboard ada di index 0
