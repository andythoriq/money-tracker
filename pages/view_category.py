from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, QCoreApplication
from controller.Popup import PopupWarning, PopupSuccess
from controller.category import Category

class CategoryView(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.category_controller = Category()
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        self.title_label = QLabel("Category")
        self.title_label.setObjectName("tittleLabel")
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
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Category Name")
        self.input_name.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        self.input_type = QComboBox()
        self.input_type.addItems(["income", "outcome"])
        self.input_type.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-width: 0px;
            }
        """)

        self.btn_add = QPushButton("Add Category")
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_add.clicked.connect(self.add_category)

        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.input_type)
        form_layout.addWidget(self.btn_add)

        content_layout.addWidget(form_widget)

        # === TABEL KATEGORI ===
        self.table = QTableWidget()
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Delete"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #7A9F60;
                border-radius: 10px;
                color: white;
                gridline-color: #98C379;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #6A8B52;
            }
            QHeaderView::section {
                background-color: #7A9F60;
                color: white;
                padding: 5px;
                border: none;
            }
            QScrollBar {
                background-color: #7A9F60;
            }
        """)
        
        # Set column widths
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 200)  # Name column
        self.table.setColumnWidth(1, 200)  # Type column
        self.table.setColumnWidth(2, 100)  # Delete column
        
        self.table.verticalHeader().setVisible(False)
        content_layout.addWidget(self.table)
        self.setStyleSheet("background-color: #98C379;")

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_categories()

    def add_category(self):
        """Menambahkan kategori baru"""
        name = self.input_name.text().strip()
        category_type = self.input_type.currentText()

        result = self.category_controller.add_category(name, category_type)

        if result.get("valid"):
            self.input_name.clear()
            self.load_categories()
            PopupSuccess("Success", "Category berhasil disimpan!")
        else:
            errors = result.get("errors")
            error_message = "\n".join([f"{key}: {value}" for key, value in errors.items()])
            PopupWarning("Warning", f"Gagal menyimpan wallet!\n{error_message}")

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
            self.btn_delete = QPushButton("Delete")
            self.btn_delete.setFixedWidth(80)
            self.btn_delete.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.btn_delete.clicked.connect(lambda _, n=name, t=category_type: self.confirm_delete(n,t))
            self.table.setCellWidget(row_idx, 2, self.btn_delete)
            # btn_delete.clicked.connect(lambda _, n=name, t=category_type: self.confirm_delete(n, t))
            # self.table.setCellWidget(row_idx, 2, btn_delete)

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
            self.input_name.setText(_translate("Form", lang.get("category", {}).get("desc", "")))
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
            self.btn_delete.setText(_translate("Form", lang.get("category", {}).get("col3", "")))