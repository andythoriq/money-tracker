import locale
import re

class NumberFormat:
    @staticmethod
    def getFormattedMoney(value, locale_str = 'id_ID'):
        try:
            # Konversi jika value bukan string
            if isinstance(value, (int, float)):
                number = value
            else:
                digits_only = re.sub(r'\D', '', str(value))
                number = int(digits_only) if digits_only else 0

            # Set locale
            try:
                locale.setlocale(locale.LC_ALL, locale_str)
            except locale.Error:
                locale.setlocale(locale.LC_ALL, '')

            return locale.format_string("%d", number, grouping=True)
        except Exception as e:
            print(f"[inputMoney Error] {e}")
            return str(value)

    @staticmethod
    def getMoney(text):
        """
        Mengambil angka asli (tanpa pemisah ribuan) dari teks.
        Misalnya: "1.000.000" => 1000000
        """
        try:
            digits_only = re.sub(r'\D', '', text)
            return int(digits_only) if digits_only else 0
        except Exception as e:
            print(f"[getMoney Error] {e}")
            return 0
