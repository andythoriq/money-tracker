from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

class PopupWarning(QMessageBox):
    def __init__(self, title, message, icon_path=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.setObjectName("PopupWarning")

        # Menambahkan ikon kustom jika diberikan
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        self.exec_()

class PopupSuccess(QMessageBox):
    def __init__(self, title, message, icon_path=None):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)
        self.setObjectName("PopupSuccess")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        self.exec_()

class PopupAboutUs(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Money Tracker")
        self.setObjectName("PopupAboutUs")

        # Set icon aplikasi
        self.setWindowIcon(QIcon("img/icon/aboutUs.png"))
        
        # Membuat pesan HTML dengan format yang lebih menarik
        about_text = """
        <div style='text-align: center;'>
            <h2 style='color: #98C379;'>Money Tracker v1.2</h2>
            <p style='font-size: 14px; color: white;'>
                Money Tracker adalah aplikasi manajemen keuangan untuk mengelola pemasukan dan
                pengeluaran Anda secara efektif dan efisien.
            </p>
            <h3 style='color: #98C379;'>Dikembangkan oleh:</h3>
            <p style='font-size: 14px; color: white;'>
                Kelompok 1A<br>
                1. Andy Thoriq Putra Sitanggang (241524004)<br>
                2. Faris Ichsan Alyawa (241524010)<br>
                3. Johan Muhammad Avicenna (241524013)<br>
                4. Wahyu Dwi Lestari (241524029)<br>
                5. Zaidan Arkaan Azharuddya Asshauqi (241524030)<br>
            </p>
        </div>
        """
        
        self.setText(about_text)
        
        # Mengatur ukuran popup
        self.setMinimumWidth(450)
        
        # Hanya menampilkan tombol OK
        self.setStandardButtons(QMessageBox.Ok)
        
        self.exec_()