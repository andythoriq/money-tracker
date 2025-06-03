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
        categories = self.load_categories()

        #validasi
        result = self.validate_category_data({'name': name, 'type': category_type})
        if result.get("valid") is False:
            return result

        categories.append({"name": name, "type": category_type})
        self.save_categories(categories)
        return result

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
        category_type = "income" if category_type == 0 else "outcome"
        if category_type not in ["income", "outcome"]:
            raise ValueError("Jenis kategori harus 'income' atau 'outcome'.")
        return [cat["name"] for cat in self.load_categories() if cat["type"] == category_type]

    def save_categories(self, categories):
        """Menyimpan kategori ke file."""
        with open(self.FILE_PATH, "w") as file:
            json.dump(categories, file, indent=4)

    def validate_category_data(self, category):
        errors = {}
        category["type"] = "income" if category == 0 else "outcome"
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