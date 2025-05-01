import os

class Category:
    FILE_PATH = "database/category.txt"

    def __init__(self):
        """Inisialisasi controller"""
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w"):
                pass  

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
        """
        Menghapus kategori berdasarkan nama.
        :param name: Nama kategori yang ingin dihapus
        :param category_type: Category yang ingin  dihapus
        """
        categories = self.load_categories()
        new_categories = [cat for cat in categories if not (cat[0] == name and cat[1] == category_type)]

        with open(self.FILE_PATH, "w") as file:
            for cat in new_categories:
                file.write(f"{cat[0]},{cat[1]}\n")

    def load_categories(self):
        """
        Memuat semua kategori dari file.
        :return: List berisi tuple (name, type)
        """
        if not os.path.exists(self.FILE_PATH):
            return []

        with open(self.FILE_PATH, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def load_category_names(self, category_type):
        """
        Memuat hanya nama kategori berdasarkan type.
        :param category_type: Jenis kategori yang diambil ('income' atau 'outcome')
        :return: List berisi nama kategori
        """
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