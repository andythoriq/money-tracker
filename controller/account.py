import json, os

class Account:
    FILE_PATH = "database/account.json"

    def __init__(self):
        """Inisialisasi controller"""
        try:
            with open(self.FILE_PATH, "r") as file:
                pass  # File sudah ada
        except FileNotFoundError:
            with open(self.FILE_PATH, "w") as file:
                json.dump([], file)

    def load_account(self):
        """
        Memuat semua akun dari file.
        :return: List berisi dictionary akun.
        """
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Jika file kosong atau tidak valid, anggap tidak ada akun
            return []

    def save_accounts(self, accounts):
        """
        Menyimpan daftar akun ke file.
        :param accounts: List berisi akun-akun
        """
        with open(self.FILE_PATH, "w") as file:
            json.dump(accounts, file)

    def add_account(self, email, name, password, gender, birth, phone):
        """
        Menambahkan akun baru.
        """
        accounts = self.load_account()
        if any(acc["email"] == email for acc in accounts):
            return False

        accounts.append(
            {
                "id": accounts[-1]["id"] + 1 if accounts else 1,
                "email": email,
                "name": name,
                "password": password,
                "gender": gender,
                "birth": birth,
                "phone": phone,
            }
        )

        self.save_accounts(accounts)
        return True

    def load_account_names(self):
        """
        Memuat hanya nama akun.
        :return: List berisi nama akun
        """
        accounts = self.load_account()
        return [acc["username"] for acc in accounts]

    def delete_account(self, username):
        """
        Menghapus akun berdasarkan nama pengguna.
        :param username: Nama pengguna yang ingin dihapus
        """
        accounts = self.load_account()
        new_accounts = [acc for acc in accounts if acc["username"] != username]

        with open(self.FILE_PATH, "w") as file:
            json.dump(new_accounts, file)

    def update_account(self, email, new_password):
        """
        Mengupdate akun berdasarkan email pengguna
        :param email: email pengguna yang ingin diupdate
        :param new_password: Kata sandi baru
        """
        accounts = self.load_account()
        for acc in accounts:
            if acc["email"] == email:
                acc["password"] = new_password
                break

        with open(self.FILE_PATH, "w") as file:
            json.dump(accounts, file)
            return True

    def check_email_exists(self, email):
        """
        Memeriksa apakah email sudah ada di database.
        :param email: Email yang ingin diperiksa
        :return: True jika email ada, False jika tidak
        """
        accounts = self.load_account()
        return any(acc["email"] == email for acc in accounts)

