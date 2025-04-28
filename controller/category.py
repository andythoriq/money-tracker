import os

class Category:
    FILE_PATH = "database/category.txt"

    def __init__(self):
        """Inisialisasi controller"""
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w"):
                pass  

    def add_category(self, name, category_type):
        """
        Menambahkan kategori baru.
        :param name: Nama kategori (string)
        :param category_type: Jenis kategori ('income' atau 'outcome')
        """
        if category_type not in ["income", "outcome"]:
            raise ValueError("Jenis kategori harus 'income' atau 'outcome'.")

        with open(self.FILE_PATH, "a") as file:
            file.write(f"{name},{category_type}\n")

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

        return [name for name, ctype in self.load_categories() if ctype == category_type]
