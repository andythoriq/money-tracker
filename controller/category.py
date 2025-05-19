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
        if category_type == 0:
            category_type = "income"
        else:
            category_type = "outcome"

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

    def validate_category_data(self, category):
        errors = {}

        if category.get('type') not in ["income", "outcome"]:
            errors["type"] = "Jenis kategori harus 'income' atau 'outcome'."

        if not category.get('name'):
            errors["name"] = "category tidak boleh kosong."
        elif category.get('name').lower() in (name.lower() for name in self.load_category_names(category.get('type'))):
            errors["name"] = "category sudah ada."
        elif len(category.get('name')) < 3:
            errors["name"] = "category harus lebih dari 3 karakter."
        elif len(category.get('name')) > 20:
            errors["name"] = "category tidak boleh lebih dari 20 karakter."
        elif not category.get('name').isalnum():
            errors["name"] = "category hanya boleh mengandung huruf dan angka."
        elif not category.get('name')[0].isalpha():
            errors["name"] = "category harus diawali dengan huruf."

        return {"valid": not bool(errors), "errors": errors}