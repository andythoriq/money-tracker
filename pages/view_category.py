from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QHeaderView 
from PyQt5.QtCore import Qt, QCoreApplication
from controller.Popup import PopupWarning, PopupSuccess
from controller.category import Category

class CategoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_controller = Category()
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        # Main container with dark background
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        self.title_label = QLabel("Category")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

        # Content Container
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # === FORM INPUT ===
        form_widget = QWidget()
        form_widget.setObjectName("groupBox")
        form_layout = QHBoxLayout(form_widget)
        form_layout.setSpacing(10)

        # Input fields
        self.name_label = QLabel("Nama:")
        self.name_label.setObjectName("form_label")

        self.input_name = QLineEdit()
        self.input_name.setObjectName("wishlist_input")
        self.input_name.setPlaceholderText("Nama kategori")
        self.input_name.setFixedWidth(400)

        self.type_label = QLabel("Tipe:")
        self.type_label.setObjectName("form_label")

        self.input_type = QComboBox()
        self.input_type.addItems(["Income", "Outcome"])
        self.input_type.setStyleSheet("""
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-width: 0px;
            }
        """)

        self.btn_add = QPushButton("Add Category")
        self.btn_add.setObjectName("add_button")
        self.btn_add.clicked.connect(self.add_category)

        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.type_label)
        form_layout.addWidget(self.input_type)
        form_layout.addWidget(self.btn_add)

        form_layout.addStretch()

        content_layout.addWidget(form_widget)

        # === TABEL KATEGORI ===
        self.table = QTableWidget()
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Delete"])
        
        # Set column widths
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 200)  # Name column
        self.table.setColumnWidth(1, 200)  # Type column
        self.table.setColumnWidth(2, 100)  # Delete column
        
        self.table.verticalHeader().setVisible(False)
        content_layout.addWidget(self.table)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_categories()

    def add_category(self):
        """Menambahkan kategori baru"""
        name = self.input_name.text().strip()
        category_type = self.input_type.currentIndex()
        category_type = "Income" if category_type == 0 else "Outcome"

        if not name:
            msg = QMessageBox()
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #98C379;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 70px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            msg.setWindowTitle("Warning")
            msg.setText("Category name cannot be empty!")
            msg.exec_()
            return

        self.category_controller.add_category(name, category_type)
        self.input_name.clear()
        self.load_categories()

    def load_categories(self):
        """Memuat ulang data kategori ke tabel"""
        self.table.setRowCount(0)
        categories = self.category_controller.load_categories()

        for row_idx, category in enumerate(categories):
            name = category["name"]
            category_type = category["type"]

            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(category_type))

            # Tombol Delete
            btn_delete = QPushButton("Delete")
            btn_delete.setFixedWidth(80)
            btn_delete.setObjectName("Delete")            
            btn_delete.clicked.connect(lambda _, n=name, t=category_type: self.confirm_delete(n, t))
            self.table.setCellWidget(row_idx, 2, btn_delete)

    def confirm_delete(self, name, category_type):
        """Popup konfirmasi sebelum menghapus kategori"""
        msg = QMessageBox()
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #98C379;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg.setWindowTitle("Delete Category")
        msg.setText(f"Are you sure you want to delete '{name}'?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        result = msg.exec_()
        if result == QMessageBox.Yes:
            self.category_controller.delete_category(name, category_type)
            self.load_categories()

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("category", {}).get("Title", "")))
            self.name_label.setText(_translate("Form", lang.get("category", {}).get("col1", "") + ":"))
            self.type_label.setText(_translate("Form", lang.get("category", {}).get("col3", "") + ":"))
            self.input_name.setPlaceholderText(_translate("Form", lang.get("category", {}).get("desc", "")))
            self.input_type.setItemText(0, lang.get("category", {}).get("item1", ""))
            self.input_type.setItemText(1, lang.get("category", {}).get("item2", ""))
            self.btn_add.setText(_translate("Form", lang.get("category", {}).get("btn", "")))
            self.table.setHorizontalHeaderLabels(
                [
                    lang.get("category", {}).get("col1", ""), 
                    lang.get("category", {}).get("col2", ""), 
                    lang.get("category", {}).get("col3", "")
                    ]
                )
            for row in range(self.table.rowCount()):
                widget = self.table.cellWidget(row, 2)
                if isinstance(widget, QPushButton):
                    widget.setText(_translate("Form", lang.get("category", {}).get("col3", "")))