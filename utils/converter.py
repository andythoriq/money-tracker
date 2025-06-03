import requests
from typing import Dict, Optional
from .number_formatter import NumberFormat

class CurrencyConverter:
    def __init__(self):
        self.base_url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"
        self.rates: Dict[str, float] = {}
        self.currency_formats = {
            'usd': {'locale': 'en_US', 'symbol': '$'},
            'eur': {'locale': 'de_DE', 'symbol': '€'},
            'gbp': {'locale': 'en_GB', 'symbol': '£'},
            'jpy': {'locale': 'ja_JP', 'symbol': '¥'},
            'idr': {'locale': 'id_ID', 'symbol': 'Rp'},
            'sgd': {'locale': 'en_SG', 'symbol': 'S$'},
            'aud': {'locale': 'en_AU', 'symbol': 'A$'},
            'cny': {'locale': 'zh_CN', 'symbol': '¥'},
            'inr': {'locale': 'en_IN', 'symbol': '₹'},
            'myr': {'locale': 'ms_MY', 'symbol': 'RM'},
            'thb': {'locale': 'th_TH', 'symbol': '฿'},
            'vnd': {'locale': 'vi_VN', 'symbol': '₫'},
            'php': {'locale': 'en_PH', 'symbol': '₱'},
            'krw': {'locale': 'ko_KR', 'symbol': '₩'},
        }
        self.update_rates()

    def update_rates(self) -> None:
        """Memperbarui nilai tukar mata uang dari API"""
        try:
            response = requests.get(f"{self.base_url}/idr.json")
            data = response.json()
            self.rates = data["idr"]
        except Exception as e:
            print(f"Error updating rates: {e}")
            self.rates = {}

    def get_available_currencies(self) -> list:
        """Mendapatkan daftar mata uang yang tersedia"""
        return list(self.rates.keys())

    def convert(self, amount: float, target_currency: str) -> Optional[float]:
        """
        Mengkonversi jumlah IDR ke mata uang target
        
        Args:
            amount (float): Jumlah dalam IDR
            target_currency (str): Kode mata uang target (contoh: 'usd', 'eur')
            
        Returns:
            float: Jumlah yang dikonversi atau None jika terjadi error
        """
        try:
            if not self.rates:
                self.update_rates()
            
            if target_currency not in self.rates:
                return None
                
            converted_amount = self.rates[target_currency] * amount
            return converted_amount
        except Exception as e:
            print(f"Error converting currency: {e}")
            return None

    def format_amount(self, amount: float, currency_code: str = 'idr') -> str:
        """
        Memformat jumlah dengan format mata uang yang sesuai menggunakan NumberFormat
        
        Args:
            amount (float): Jumlah yang akan diformat
            currency_code (str): Kode mata uang (contoh: 'usd', 'eur')
            
        Returns:
            str: Jumlah yang diformat dengan simbol mata uang
        """
        try:
            # Dapatkan format mata uang
            currency_format = self.currency_formats.get(currency_code.lower(), 
                                                      {'locale': 'en_US', 'symbol': currency_code.upper()})
            
            # Format jumlah menggunakan NumberFormat
            formatted_number = NumberFormat.getFormattedMoney(amount, currency_format['locale'])
            
            # Tambahkan simbol mata uang
            if currency_code.lower() in ['jpy', 'krw', 'vnd']:
                # Mata uang yang tidak menggunakan desimal
                return f"{currency_format['symbol']} {formatted_number}"
            else:
                # Mata uang yang menggunakan desimal
                return f"{currency_format['symbol']} {formatted_number}"
            
        except Exception as e:
            print(f"Error formatting currency: {e}")
            # Fallback format jika terjadi error
            return f"{currency_code.upper()} {amount:,.2f}"

def main():
    """Fungsi main untuk testing"""
    converter = CurrencyConverter()
    print("Ubah IDR ke mata uang lain!")
    print("List mata uang:")
    print("")
    for currency in converter.get_available_currencies():
        print(currency)
    
    source = input("Masukan Mata uang tujuan: ").lower()
    amount = float(input("Masukan Jumlah IDR: "))
    
    converted = converter.convert(amount, source)
    if converted is not None:
        formatted = converter.format_amount(converted, source)
        print(f"{converter.format_amount(amount, 'idr')} = {formatted}")
    else:
        print("Konversi gagal. Pastikan mata uang tujuan valid.")

if __name__ == "__main__":
    main()

