from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QLabel, QRadioButton, 
    QButtonGroup, QDialog, QFormLayout, QSpinBox, 
    QComboBox, QLineEdit, QCalendarWidget, QMessageBox, 
    QTableView, QVBoxLayout, QDateEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QDate, QCoreApplication
from datetime import datetime
from controller.income import Income
from controller.outcome import Outcome
from controller.wallet import Wallet
from controller.category import Category
from controller.Popup import PopupWarning, PopupSuccess
from utils.converter import CurrencyConverter

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallet_controller = Wallet()
        self.category_controller = Category()
        self.income_controller = Income(self.wallet_controller)
        self.outcome_controller = Outcome(self.wallet_controller)
        self.currency_converter = CurrencyConverter()
        self.init_ui()
        self.setObjectName("HomeSection")

    def init_ui(self):
        """Inisialisasi UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title Section
        self.title_label = QLabel("History")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

        # Content Container
        content_widget = QWidget()
        content_widget.setObjectName("Layout")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Radio Button Filter
        filter_widget = QWidget()
        filter_widget.setObjectName("groupBox")
        btn_layout = QHBoxLayout(filter_widget)
        btn_layout.setSpacing(10)
        self.radio_group = QButtonGroup(self)

        self.filter_label = QLabel("Filter Jenis:")
        self.filter_label.setObjectName("form_label")
        self.radio_all = QRadioButton("Semua")
        self.radio_all.setObjectName("radio_button")
        self.radio_income = QRadioButton("Income")
        self.radio_income.setObjectName("radio_button")
        self.radio_outcome = QRadioButton("Outcome")
        self.radio_outcome.setObjectName("radio_button")
        
        # Search bar untuk kategori
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Cari kategori")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_by_category)

        # Date Edit untuk filter tanggal
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #7A9F60;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QDateEdit::down-arrow {
                border: none;
                width: 16px;
                height: 16px;
                image: url(img/down-arrow.png);
            }
            QDateEdit::down-arrow:enabled {
                border: none;
                width: 16px;
                height: 16px;
                image: url(img/icon1.png);
            }
            QCalendarWidget {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
            }
            QCalendarWidget QToolButton {
                background-color: #7A9F60;
                color: white;
                border-radius: 5px;
            }
            QCalendarWidget QMenu {
                background-color: white;
            }
        """)
        self.date_edit.dateChanged.connect(self.filter_by_date)
        self.selected_date = None

        for radio in [self.radio_all, self.radio_income, self.radio_outcome]:
            radio.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 14px;
                    padding: 5px;
                }
                QRadioButton::indicator {
                    width: 15px;
                    height: 15px;
                }
            """)

        self.radio_group.addButton(self.radio_all)
        self.radio_group.addButton(self.radio_income)
        self.radio_group.addButton(self.radio_outcome)

        self.radio_all.setChecked(True)
        self.radio_income.toggled.connect(lambda: self.load_data("Income"))
        self.radio_outcome.toggled.connect(lambda: self.load_data("Outcome"))
        self.radio_all.toggled.connect(lambda: self.load_data("all"))
        
        btn_layout.addWidget(self.filter_label)
        btn_layout.addWidget(self.radio_all)
        btn_layout.addWidget(self.radio_income)
        btn_layout.addWidget(self.radio_outcome)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.search_bar)
        btn_layout.addWidget(self.date_edit)

        # Tambahkan ComboBox untuk pemilihan mata uang
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(self.currency_converter.get_available_currencies())
        self.currency_combo.setCurrentText("idr")  # Default ke IDR
        self.currency_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #7A9F60;
                border-radius: 5px;
                padding: 5px;
                color: black;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #7A9F60;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
        """)
        self.currency_combo.currentTextChanged.connect(self.update_currency_display)
        self.labelkurs = QLabel("Mata Uang:")
        self.labelkurs.setObjectName("labelkurs")
        btn_layout.addWidget(self.labelkurs)
        btn_layout.addWidget(self.currency_combo)

        # Tombol Hapus Filter
        self.clear_filter_btn = QPushButton("Refresh Filter")
        self.clear_filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        btn_layout.addWidget(self.clear_filter_btn)

        content_layout.addWidget(filter_widget)

        # Tabel Transaksi
        self.table = QTableWidget()
        self.table.setObjectName("table")
        self.table.setColumnCount(8)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.table.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Jumlah", "Kategori", "Dompet", "Deskripsi", "Edit", "Delete"])
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        content_layout.addWidget(self.table)

        # Label Total
        self.label = QLabel("Total : Rp 0")
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignRight)
        content_layout.addWidget(self.label)

        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
        self.load_data("all")

    def filter_by_date(self, date):
        """Filter data berdasarkan tanggal"""
        self.selected_date = date
        self.apply_filters()

    def filter_by_category(self):
        """Filter data berdasarkan kategori"""
        self.apply_filters()

    def apply_filters(self):
        """Menerapkan semua filter yang ada"""
        search_text = self.search_bar.text().lower()
        
        for row in range(self.table.rowCount()):
            category_item = self.table.item(row, 3)  # Kolom kategori
            date_item = self.table.item(row, 0)      # Kolom tanggal
            
            show_row = True
            
            # Filter kategori
            if search_text and category_item:
                category = category_item.text().lower()
                show_row = show_row and (search_text in category)
            
            # Filter tanggal
            if self.selected_date and date_item:
                try:
                    row_date = datetime.strptime(date_item.text(), "%d/%m/%Y").date()
                    show_row = show_row and (row_date == self.selected_date.toPyDate())
                except ValueError:
                    show_row = False
            
            self.table.setRowHidden(row, not show_row)

    def update_currency_display(self):
        """Memperbarui tampilan jumlah dengan mata uang yang dipilih"""
        selected_currency = self.currency_combo.currentText()
        
        for row in range(self.table.rowCount()):
            amount_item = self.table.item(row, 2)
            if amount_item:
                # Ekstrak nilai numerik dari string
                amount_str = amount_item.text().replace("Rp ", "").replace(".", "")
                try:
                    amount = float(amount_str)
                    converted = self.currency_converter.convert(amount, selected_currency)
                    if converted is not None:
                        formatted = self.currency_converter.format_amount(converted, selected_currency)
                        amount_item.setText(formatted)
                except ValueError:
                    continue

        # Update total
        if hasattr(self, 'total'):
            converted_total = self.currency_converter.convert(self.total, selected_currency)
            if converted_total is not None:
                formatted_total = self.currency_converter.format_amount(converted_total, selected_currency)
                self.label.setText(f"Total : {formatted_total}")

    def load_data(self, filter_type):
        """Memuat data ke tabel berdasarkan filter"""
        self.table.setRowCount(0)
        transactions = []
        self.total = 0

        # Load data income
        for income in self.income_controller.load_incomes():
            transactions.append({
                "id": income.get("ID"),
                "date": datetime.strptime(income.get("date"), "%d/%m/%Y"),
                "type": "Income",
                "amount": income.get("amount"),
                "category": income.get("category"),
                "wallet": income.get("wallet"),
                "desc": income.get("desc")
            })

        # Load data outcome
        for outcome in self.outcome_controller.load_outcomes():
            transactions.append({
                "id": outcome.get("ID"),
                "date": datetime.strptime(outcome.get("date"), "%d/%m/%Y"),
                "type": "Outcome",
                "amount": outcome.get("amount"),
                "category": outcome.get("category"),
                "wallet": outcome.get("wallet"),
                "desc": outcome.get("desc")
            })

        # Filter transaksi
        if self.radio_all.isChecked():
            transactions = [t for t in transactions]
        elif filter_type == "Income":
            transactions = [t for t in transactions if t["type"] == "Income"]
        elif filter_type == "Outcome":
            transactions = [t for t in transactions if t["type"] == "Outcome"]

        transactions.sort(key=lambda x: x["date"], reverse=True)

        # Tampilkan data di tabel
        self.table.setRowCount(len(transactions))
        for row, transaction in enumerate(transactions):
            if transaction["type"] == "Income":
                self.total += int(transaction["amount"])
            else:
                self.total -= int(transaction["amount"])

            self.table.setItem(row, 0, QTableWidgetItem(transaction["date"].strftime("%d/%m/%Y")))
            self.table.setItem(row, 1, QTableWidgetItem(transaction["type"]))

            # Konversi dan format jumlah
            selected_currency = self.currency_combo.currentText()
            converted = self.currency_converter.convert(int(transaction["amount"]), selected_currency)
            if converted is not None:
                formatted = self.currency_converter.format_amount(converted, selected_currency)
                self.table.setItem(row, 2, QTableWidgetItem(formatted))
            else:
                self.table.setItem(row, 2, QTableWidgetItem(self.currency_converter.format_amount(int(transaction["amount"]), 'idr')))
            self.table.setItem(row, 3, QTableWidgetItem(transaction["category"]))
            self.table.setItem(row, 4, QTableWidgetItem(transaction["wallet"]))
            self.table.setItem(row, 5, QTableWidgetItem(transaction["desc"]))

            # Tombol Edit
            btn_edit = QPushButton()
            btn_edit.setObjectName("Edit")
            btn_edit.clicked.connect(lambda _, t=transaction: self.open_edit_popup(t))
            self.table.setCellWidget(row, 6, btn_edit)

            # Tombol Delete
            btn_delete = QPushButton()
            btn_delete.setObjectName("Delete")
            btn_delete.clicked.connect(lambda _, t=transaction: self.confirm_delete(t))
            self.table.setCellWidget(row, 7, btn_delete)

        # Update total dengan mata uang yang dipilih
        selected_currency = self.currency_combo.currentText()
        converted_total = self.currency_converter.convert(self.total, selected_currency)
        if converted_total is not None:
            formatted_total = self.currency_converter.format_amount(converted_total, selected_currency)
            self.label.setText(f"Total : {formatted_total}")
        else:
            self.label.setText(f"Total : {self.currency_converter.format_amount(self.total, 'idr')}")

    def open_edit_popup(self, transaction):
        """Popup Edit Data"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Transaksi")

        layout = QFormLayout(dialog)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Widget Form
        amount_input = QSpinBox()
        amount_input.setMaximum(100000000)
        amount_input.setValue(int(transaction["amount"]))

        category_input = QComboBox()
        category_input.addItems(self.category_controller.load_category_names(transaction["type"]))
        category_input.setCurrentText(transaction["category"])

        wallet_input = QComboBox()
        wallet_input.addItems(self.wallet_controller.get_wallet_name())
        wallet_input.setCurrentText(transaction["wallet"])

        desc_input = QLineEdit(transaction["desc"])

        date_input = QCalendarWidget()
        date_input.setSelectedDate(transaction["date"])

        layout.addRow("Jumlah:", amount_input)
        layout.addRow("Kategori:", category_input)
        layout.addRow("Dompet:", wallet_input)
        layout.addRow("Deskripsi:", desc_input)
        layout.addRow("Tanggal:", date_input)

        # Tombol Simpan
        btn_save = QPushButton("Simpan")
 
        btn_save.clicked.connect(lambda: self.save_edit(transaction, amount_input, category_input, wallet_input, desc_input, date_input, dialog))
        layout.addRow(btn_save)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_edit(self, transaction, amount, category, wallet, desc, date, dialog):
        """Simpan perubahan edit transaksi"""
        new_data = {
            "ID": transaction["id"],
            "amount": amount.value(),
            "category": category.currentText(),
            "wallet": wallet.currentText(),
            "desc": desc.text(),
            "date": date.selectedDate().toString("dd/MM/yyyy")
        }

        if transaction["type"] == "Income":
            self.income_controller.update_income(new_data)
        else:
            self.outcome_controller.update_outcome(new_data)

        dialog.accept()
        self.load_data(transaction["type"])

    def confirm_delete(self, transaction):
        """Konfirmasi Delete"""
        msg = QMessageBox()
        msg.setStyleSheet("""  
         QPushButton {
                background-color: #000000;
                color: white;
                border-radius: 5px;
                padding: 5px;
                min-width: 70px;
            }""")
        msg.setWindowTitle("Konfirmasi Hapus")
        msg.setText(f"Apakah Anda yakin ingin menghapus transaksi {transaction['type']} dengan jumlah Rp {transaction['amount']}?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        result = msg.exec_()
        if result == QMessageBox.Yes:
            if transaction["type"] == "Income":
                self.income_controller.delete_income(transaction["id"])
            else:
                self.outcome_controller.delete_outcome(transaction["id"])

            self.load_data(transaction["type"])
            
            info_msg = QMessageBox()
            info_msg.setStyleSheet(msg.styleSheet())
            info_msg.setWindowTitle("Informasi")
            info_msg.setText("Transaksi berhasil dihapus")
            info_msg.exec_()

    def clear_filters(self):
        """Mengembalikan semua filter ke setelan awal"""
        # Reset radio button
        self.radio_all.setChecked(True)
        
        # Reset search bar
        self.search_bar.clear()
        
        # Reset date filter
        self.date_edit.setDate(QDate.currentDate())
        self.selected_date = None
        
        # Tampilkan semua data
        self.load_data("all")

    def retranslateUi(self, lang=None):
        _translate = QCoreApplication.translate
        if lang:
            self.title_label.setText(_translate("Form", lang.get("history", {}).get("Title", "")))
            self.filter_label.setText(_translate("Form", lang.get("history", {}).get("label", "") + ":"))
            self.labelkurs.setText(_translate("Form", lang.get("history", {}).get("label2", "") + ":"))
            self.clear_filter_btn.setText(_translate("Form", lang.get("history", {}).get("btn1", "")))
            self.radio_all.setText(_translate("Form", lang.get("history", {}).get("radbtn1", "")))
            self.radio_income.setText(_translate("Form", lang.get("history", {}).get("radbtn2", "")))
            self.radio_outcome.setText(_translate("Form", lang.get("history", {}).get("radbtn3", "")))
            self.table.setHorizontalHeaderLabels(
                [
                    lang.get("history", {}).get("col1", ""), 
                    lang.get("history", {}).get("col2", ""), 
                    lang.get("history", {}).get("col3", ""), 
                    lang.get("history", {}).get("col4", ""), 
                    lang.get("history", {}).get("col5", ""), 
                    lang.get("history", {}).get("col6", ""), 
                    lang.get("history", {}).get("col7", ""), 
                    lang.get("history", {}).get("col8", ""), 
                    ]
                )
            self.label.setText(_translate("Form", lang.get("history", {}).get("foot", "") + f"Rp {self.total}"))
            for row in range(self.table.rowCount()):
                widget = self.table.cellWidget(row, 6)
                if isinstance(widget, QPushButton):
                    widget.setText(_translate("Form", lang.get("history", {}).get("col7", "")))
            for row in range(self.table.rowCount()):
                widget = self.table.cellWidget(row, 7)
                if isinstance(widget, QPushButton):
                    widget.setText(_translate("Form", lang.get("history", {}).get("col8", "")))
