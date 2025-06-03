from PyQt5.QtWidgets import QLineEdit
from utils.number_formatter import NumberFormat

class MoneyLineEdit(QLineEdit):
    def __init__(self, locale_str='id_ID'):
        super().__init__()
        self.locale_str = locale_str
        self.textEdited.connect(self.on_text_edited)
        self._last_text = ""

    def on_text_edited(self, text):
        cursor_pos = self.cursorPosition()

        # Format input
        formatted = NumberFormat.getFormattedMoney(text, self.locale_str)

        # Update field tanpa memicu sinyal berulang
        self.blockSignals(True)
        self.setText(formatted)
        self.blockSignals(False)

        # Perbarui posisi kursor (tidak sempurna, tapi cukup untuk angka pendek)
        new_cursor_pos = len(formatted) - (len(self._last_text) - cursor_pos)
        self.setCursorPosition(max(0, new_cursor_pos))
        self._last_text = formatted

    def get_value(self) -> int:
        """
        Mendapatkan nilai angka raw (tanpa format)
        """
        return NumberFormat.getMoney(self.text())

    def set_value(self, value: int):
        """
        Atur nilai langsung dalam format angka
        """
        formatted = NumberFormat.getFormattedMoney(value, self.locale_str)
        self.blockSignals(True)
        self.setText(formatted)
        self.blockSignals(False)
        self._last_text = formatted