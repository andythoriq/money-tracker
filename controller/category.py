import json

class Category:
    FILE_PATH = "database/category.json"

    def __init__(self):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)

    def add_category(self, name, category_type):
        """Menambahkan kategori baru."""
        if category_type not in ["income", "outcome"]:
            raise ValueError("Jenis kategori harus 'income' atau 'outcome'.")

        categories = self.load_categories()
        categories.append({"name": name, "type": category_type})
        self.save_categories(categories)

    def delete_category(self, name, category_type):
        """Menghapus kategori berdasarkan nama."""
        categories = self.load_categories()
        categories = [cat for cat in categories if not (cat["name"] == name and cat["type"] == category_type)]
        self.save_categories(categories)

    def load_categories(self):
        """Memuat semua kategori dari file."""
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_category_names(self, category_type):
        """Memuat hanya nama kategori berdasarkan type."""
        if category_type not in ["income", "outcome"]:
            raise ValueError("Jenis kategori harus 'income' atau 'outcome'.")
        return [cat["name"] for cat in self.load_categories() if cat["type"] == category_type]

    def save_categories(self, categories):
        """Menyimpan kategori ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(categories, file, indent=4)
